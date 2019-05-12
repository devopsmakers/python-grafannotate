# `grafannotate`

[![Build Status](https://travis-ci.org/devopsmakers/python-grafannotate.svg?branch=master)](https://travis-ci.org/devopsmakers/python-grafannotate)
[![Coverage Status](https://coveralls.io/repos/github/devopsmakers/python-grafannotate/badge.svg?branch=master)](https://coveralls.io/github/devopsmakers/python-grafannotate?branch=master)
[![PyPI version](https://badge.fury.io/py/grafannotate.svg)](https://badge.fury.io/py/grafannotate)

A CLI tool to send Grafana annotations to various destinations.

## Installation
```
pip install grafannotate
```

## Usage

```
grafannotate --help
Usage: grafannotate [OPTIONS]

  Send Grafana annotations

Options:
  -u, --uri TEXT          URI to send annotation to. Default:
                          "http://localhost:3000/api/annotations".
  -T, --title TEXT        Event title. Default: "event".
  -t, --tag TEXT          Event tags (can be used multiple times).
  -d, --description TEXT  Event description body. Optional.
  -s, --start INTEGER     Start timestamp (unix secs). Default: current
                          timestamp.
  -e, --end INTEGER       End timestamp (unix secs). Optional.
  --help                  Show this message and exit.
  ```

### Examples
1. Send an annotation to Grafana API for current time
```
grafannotate --uri http://user:password@grafana:3000/api/annotations --tag my_tag --title "Event Title"
```

2. Send an annotation to Grafana API for a time region
```
grafannotate --uri http://user:password@grafana:3000/api/annotations --tag my_tag --title "Event Title" --start 1557222057 --end 1557222259
```

3. Send an annotation to Grafana API with an extended description
```
grafannotate --uri http://user:password@grafana:3000/api/annotations --tag my_tag --title "Event Title" --description "Some longer description<br />with newlines<br />and <a href=\"https://something.com/\">links</a>"
```

4. Pipe output to an annotation description
```
START_TIME=`date +%s`
command_with_output | grafannotate --uri http://user:password@grafana:3000/api/annotations --tag my_tag --title "Event Title" --start $START_TIME
```
