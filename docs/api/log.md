- [Log](#log)
  - [Retrieve logs](#retrieve-logs)
  - [Retrieve log statistics](#retrieve-log-statistics)

# Log

The log is a MongoDB persisted record of activity within HeliosBurn. This can be useful for debugging, security auditing, and general insight into the operation of the software components.

## Retrieve logs

To retrieve a list of log entries, an application submits an HTTP GET request to the URL that represents the Log resource. To avoid retrieving more logs than desirable, optional query string arguments are available to limit the results.

### Request

#### URL examples
- `/log/`: Retrieve all log entries
- `/log/?start=1&limit=500`: Retrieve the first 500 log entries
- `/log/?component=api.views.user`: Retrieve logs specific to `api.views` component(s)
- `/log/?component=api.views.user&levels=info,debug`: Retrieve logs specific to `api.views` component(s) with `info` or `debug` levels.
- `/log/?from=2015-04-01&to=2015-04-02`: Retrieve logs between *2015-04-01* and *2015-04-02*

#### Method
GET

#### Query string arguments to limit results
The following query string arguments are supported:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| start | NO | Integer | Log entries returned begin at this sequence(default is 0). |
| limit | NO | Integer | Log entries returned end at this limit beyond `start`(default is 1000). |
| component | NO | String | Restrict log entries returned to a component, matching the expression provided. |
| levels | NO | String | Comma separated list of log levels to return. |
| msg | NO | String | String to match in the `msg` field of log entries. |
| from | NO | ISODate | Time stamp that logs should be retrieved *after* |
| to | NO | ISODate | Time stamp that logs should be retrieved *before* |

### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Response Body

The response body contains a `log` key containing a list of log entries, ordered most recent to least recent. A `matchedEntries` key provides the number of log entries that matched your query.

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The log entries are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
{
  "log": [
    {
      "username": "vagrant",
      "traceback": null,
      "name": "hb.logger",
      "level": "info",
      "args": [

      ],
      "filename": "/home/vagrant/HeliosBurn/heliosburn/django/hbproject/api/views/auth.py",
      "line_no": 48,
      "time": "2015-04-15T19:24:33.683184",
      "msg": "login success for user \"admin\"",
      "funcname": "login",
      "hostname": "heliosburn-vm"
    },
    {
      "username": "vagrant",
      "traceback": null,
      "name": "hb.logger",
      "level": "info",
      "args": [

      ],
      "filename": "/home/vagrant/HeliosBurn/heliosburn/django/hbproject/api/views/auth.py",
      "line_no": 48,
      "time": "2015-04-15T19:24:34.258393",
      "msg": "login success for user \"admin\"",
      "funcname": "login",
      "hostname": "heliosburn-vm"
    }
  ],
  "matchedEntries": 231
}
```

## Retrieve log statistics

To retrieve statistics about log entries, an application submits an HTTP GET request to the URL that represents the Log resource statistics.

### Request

#### URL
- `/log/stats/`: Retrieve log entries

#### Method
GET

### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Response Body

The response body contains a JSON representing Log statistics.

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The log statistics are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
{
    "levels":[
        "info"
        ],
    "components":[
        "heliosburn",
        "hb.logger",
        "api.views.auth",
        "api.views.recording",
        "api.views.rule",
        "api.views.session",
        "api.views.testplan",
        "api.views.testplan_rule",
        "api.views.user"
        ],
    "entries": 572
}
```
