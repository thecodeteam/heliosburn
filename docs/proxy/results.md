# Module Metrics
Each module will collect statistical measurements over a given session of operation. Those results will be available via the API, by retrieving the results document for a given session.

Each module will collect the set of metrics appropriate for the respective modules execution. Those metrics will be stored in a results document in mongo at a configurable frequency that is less than once per request. Furthermore, any `status` request on the `proxy` management queue (i.e. redis queu) will contain the current statistical results.

A results document is defined as follows:


### Results Document `key` descriptions
| Key         | Description                                                                                                               |
|:------------|:--------------------------------------------------------------------------------------------------------------------------|
| id          | A unique mongo generated id                                                                                               |
| session_id  | the unique session to which the results correspond                                                                        |
| module_name | Name of the module to which the results correspond                                                                        |
| createdAt   | Timestamp corresponding to document creation                                                                              |
| metrics     | List of metrics/values dictionaries. Where `metric` is the name of the metric collected and `value` is the measured value |

### Statistical Results document
```json
{
  "id": "", -- Generated
  "session_id": "",
  "module_name": "",
  "createdAt": "",
  "metrics":
      [
          {
            "metric": "",
            "value":
        }
      ]
  }
```


### Statistical Results Example
```json
{
  "id": "0xdeadbeef",
  "session_id": "0xdeadbeefff",
  "module_name": "qos",
  "createdAt": "2014-02-12 03:34:51",
  "metrics":
      [
          {
            "metric": "requests_dropped",
            "value": 50
        },
          {
            "metric": "average_latency",
            "value": 300
        }
      ]
  }
```
