- [Log](#log)
  - [Retrieve logs](#retrieve-logs)

# Log

The log is a MongoDB persisted record of activity within HeliosBurn. This can be useful for debugging, security auditing, and general insight into the operation of the software components.

## Retrieve logs

To retrieve a list of log entries, an application submits an HTTP GET request to the URL that represents the Log resource. To avoid retrieving more logs than desirable, optional query string arguments `start` and `offset` are available to limit the results.

### Request

#### URL
- `/log/`: Retrieve all log entries
- `/log/?start=1&offset=500`: Retrieve the first 500 log entries

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

The response body contains a `log` key containing a list of log entries.

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of log entries are in the response body. |
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
  ]
}
```