import sys
import click
import logging
import time

from grafannotate.annotation import Annotation

CURRENT_TIMESTAMP = int(time.time())


@click.command()
@click.option('-u', '--uri', 'annotate_uri',
              default='http://localhost:3000/api/annotations',
              help='URI to send annotation to. Default: "http://localhost:3000/api/annotations".')
@click.option('-k', '--api-key', 'api_key', default=None,
              help='Grafana API key to pass in Authorisation header')
@click.option('-T', '--title', 'title', default='event', help='Event title. Default: "event".')
@click.option('-t', '--tag', 'tags', multiple=True, help='Event tags (can be used multiple times).')
@click.option('-d', '--description', 'description', help='Event description body. Optional.')
@click.option('-s', '--start', 'start_time', default=CURRENT_TIMESTAMP,
              help='Start timestamp (unix secs). Default: current timestamp.')
@click.option('-e', '--end', 'end_time', default=CURRENT_TIMESTAMP,
              help='End timestamp (unix secs). Optional.')
@click.option('--debug/--no-debug', default=False,
              help='Set debug logging on')
def main(annotate_uri, api_key, title, tags, description, start_time, end_time, debug):
    """
    Send Grafana annotations to various endpoints
    """

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format=' [%(levelname)s] %(message)s', level=log_level)

    try:
        if description is None:
            if not sys.stdin.isatty():
                description = "".join([line for line in iter(sys.stdin.readline, '')])
            else:
                description = ""

        this_annotation = Annotation(title, tags, description, start_time, end_time)
        result = this_annotation.send(annotate_uri, api_key)

        if result['event_data']:
            logging.debug(result['event_data'])
        if result['message']:
            logging.info(result['message'])

    except Exception as e:
        logging.exception(e)
        """
        We could exit 1 here but we really don't want to cause a job to
        fail just because we couldn't send an event.
        """

    sys.exit(0)
