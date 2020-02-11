import requests
import time
from influxdb import InfluxDBClient
from urllib.parse import urlparse

CURRENT_TIMESTAMP = int(time.time())


class Annotation:
    """
    An annotation that we want to create
    """
    def __init__(self, title, tags, description='', start=CURRENT_TIMESTAMP, end=CURRENT_TIMESTAMP):
        if len(tags) == 0:
            raise ValueError('Annotations must have at least one tag.')

        if end < start:
            raise ValueError('Annotation end time cannot be before start time.')

        self.title = title
        self.tags = tags
        self.description = description
        self.start = start
        self.end = end

    def web(self):
        """
        Returns an annotation object formatted for grafana API
        """
        annotation_event = {}
        annotation_event['text'] = '<b>%s</b>\n\n%s' % (self.title, self.description)
        annotation_event['tags'] = self.tags
        annotation_event['time'] = int(round(self.start * 1000))
        if self.start < self.end:
            annotation_event['isRegion'] = True
            annotation_event['timeEnd'] = int(round(self.end * 1000))
        return annotation_event

    def influxdb(self):
        """
        Returns an annotation object formatted for InfluxDB
        """
        tags_field = ';'.join(self.tags)
        annotation_event = {}
        annotation_event['measurement'] = 'events'
        annotation_event['fields'] = {
            'title': self.title,
            'text': self.description,
            'tags': tags_field
        }
        return [annotation_event]

    def send(self, url, api_key):
        """
        Send the annotation to a destination based on url
        """
        url_parts = urlparse(url)
        if 'http' in url_parts.scheme:
            return self.send_to_web(url_parts, api_key)
        elif 'influx' in url_parts.scheme:
            return self.send_to_influxdb(url_parts)
        else:
            raise NotImplementedError('Scheme %s not recognised in uri %s' %
                                      (url_parts.scheme, url))

    def send_to_web(self, url_parts, api_key):
        """
        POST event to an endpoint in Grafana Annotations API format
        """
        event_data = self.web()
        result_data = {'event_data': event_data}
        url = url_parts.geturl()
        auth_tuple = None
        req_headers = {}
        if api_key is not None:
            req_headers['Authorization'] = "Bearer %s" % api_key

        if url_parts.username and url_parts.password:
            auth_tuple = (url_parts.username, url_parts.password)
            url_host_port = url_parts.netloc.split('@')[1]
            url = '%s://%s%s' % (url_parts.scheme, url_host_port, url_parts.path)

        post_result = requests.post(url, json=event_data, auth=auth_tuple, headers=req_headers, timeout=5)

        if post_result.status_code > 299:
            raise Exception('Received %s response, sending event failed' % post_result.status_code)

        if 'id' in post_result.json():
            result_data['id'] = post_result.json()['id']

        if 'message' in post_result.json():
            result_data['message'] = post_result.json()['message']

        return result_data

    def send_to_influxdb(self, url_parts):
        event_data = self.influxdb()
        result_data = {'event_data': event_data}
        client = InfluxDBClient(url_parts.hostname,
                                url_parts.port or 8086,
                                url_parts.username or '',
                                url_parts.password or '',
                                url_parts.path.replace('/', '', 1) or 'events')

        if client.write_points(event_data):
            result_data['message'] = 'Annotation added'
        else:
            result_data['message'] = 'Annotation failed'

        return result_data
