import pytest
import time
import mock
import requests_mock

from grafannotate.annotation import Annotation

CURRENT_TIMESTAMP = int(time.time())


def test_annotation_without_values():
    with pytest.raises(TypeError):
        Annotation()


def test_annotation_without_tags():
    with pytest.raises(ValueError, match='must have at least one tag.'):
        Annotation('event', [], '')


def test_annotation_without_times():
    test_annotation = Annotation('event', ['events'], '')
    assert test_annotation.start == test_annotation.end


def test_annotation_with_bad_end_time():
    with pytest.raises(ValueError, match='end time cannot be before start time.'):
        Annotation('event', ['test'], '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP - 300)


def test_annotation_web():
    start_time = CURRENT_TIMESTAMP
    end_time = CURRENT_TIMESTAMP + 600
    test_annotation = Annotation('event', ['test'], 'testing', start_time, end_time)
    test_web_annotation = test_annotation.web()
    assert test_web_annotation['time'] == int(round(start_time * 1000))
    assert test_web_annotation['timeEnd'] == int(round(end_time * 1000))
    assert test_web_annotation['isRegion'] is True
    assert test_web_annotation['tags'] == ['test']
    assert test_web_annotation['text'] == '<b>event</b>\n\ntesting'


def test_annotation_influxdb():
    start_time = CURRENT_TIMESTAMP
    end_time = CURRENT_TIMESTAMP + 600
    test_annotation = Annotation('event', ['test', 'influx'], 'testing', start_time, end_time)
    test_influxdb_annotation = test_annotation.influxdb()
    assert test_influxdb_annotation[0]['measurement'] == 'events'
    assert test_influxdb_annotation[0]['fields'] == {
        'tags': 'test;influx',
        'text': 'testing',
        'title': 'event'
    }


def test_annotation_fail_to_send_to_web():
    url = "http://user:pass@localhost"
    test_annotation = Annotation('event', ['test'], 'testing')
    with pytest.raises(Exception, match='NewConnectionError'):
        test_annotation.send(url, None)


def test_annotation_send_to_web():
    url = "http://localhost:3000/api/annotations"
    with requests_mock.Mocker() as m:
        m.register_uri(
            requests_mock.POST,
            url,
            status_code=200,
            json={'message': 'Annotation added'}
        )
        test_annotation = Annotation('event', ['test'], 'testing', 1559332960, 1559332970)
        assert test_annotation.send(url, None) == {
            'event_data': {
                'isRegion': True,
                'tags': ['test'],
                'text': '<b>event</b>\n\ntesting',
                'time': 1559332960000,
                'timeEnd': 1559332970000
            },
            'message': 'Annotation added'
        }


def test_annotation_send_to_web_with_api_key():
    url = "http://localhost:3000/api/annotations"
    api_key = "307c1ac4-4e7c-4eb4-a56f-3547eeff0e4b"
    with requests_mock.Mocker() as m:
        m.register_uri(
            requests_mock.POST,
            url,
            request_headers={'Authorization': "Bearer %s" % api_key},
            status_code=200,
            json={'message': 'Annotation added'}
        )
        test_annotation = Annotation('event', ['test'], 'testing', 1559332960, 1559332970)
        assert test_annotation.send(url, api_key) == {
            'event_data': {
                'isRegion': True,
                'tags': ['test'],
                'text': '<b>event</b>\n\ntesting',
                'time': 1559332960000,
                'timeEnd': 1559332970000
            },
            'message': 'Annotation added'
        }


def test_annotation_error_sending_to_web():
    url = "http://localhost:3000/api/annotations"
    with requests_mock.Mocker() as m:
        m.register_uri(
            requests_mock.POST,
            url,
            status_code=400
        )
        test_annotation = Annotation('event', ['test'], 'testing', 1559332960, 1559332960)
        with pytest.raises(Exception, match='Received 400 response, sending event failed'):
            test_annotation.send(url, None)


def test_annotation_fail_to_send_to_influxdb():
    url = "influx://user:pass@localhost"
    test_annotation = Annotation('event', ['test'], 'testing')
    with pytest.raises(Exception, match='Failed to establish a new connection'):
        test_annotation.send(url, None)


@mock.patch('grafannotate.annotation.InfluxDBClient')
def test_annotation_send_to_influxdb(mock_influxdbclient):
    url = "influx://user:pass@localhost"
    test_annotation = Annotation('event', ['test'], 'testing')
    mock_influxdbclient.write_points.return_value = True
    assert test_annotation.send(url, None) == {
        'event_data': [{
            'fields': {
                'tags': 'test',
                'text': 'testing',
                'title': 'event'
            },
            'measurement': 'events'
        }],
        'message': 'Annotation added'
    }


def test_annotation_send_bad_url():
    url = "s3://user:pass@localhost"
    test_annotation = Annotation('event', ['test'], 'testing')
    with pytest.raises(NotImplementedError, match='Scheme s3 not recognised'):
        test_annotation.send(url, None)
