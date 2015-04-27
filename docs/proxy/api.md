The Helios Burn Proxy Interface API is used to control the state of the proxy. The following operations are currently supported:
- [Stop](#stop)
- [Start](#start)
- [Reset Modules](#reset)
- [Reload Modules](#reload)
- [Set Upstream Host](#upstream_host)
- [Set Upstream Port](#upstream_port)
- [Set Bind Host](#bind_host)
- [Set Bind Port](#bind_port)
- [Set Start Recording](#start_recording)
- [Set Stop Recording](#stop_recording)
- [Get Status](#stop_recording)
- [Run Tests](#test)


Clients publish operations to a REDIS PUBSUB channel to which the Helios Burn Proxy service is subscribed. When the proxy receives a message an appropriate action is taken and then a response sent to a subsequent REDIS PUBSUB channel. The general structure of the operation and response messages are as follows:

#### Operation Message

```json
{
    "operation": "operation string",
    "param": "operation paramater",
    "key": "response key"
}
```

#### Response Message

```json
{
    "code": "response code",
    "message": "description of response code",
    "key": "response key"
}
```



# Stop

The proxy can be stopped by publishing a proxy API operation message to the `proxy_mgmt_request` REDIS pubs channel with the operation `stop`. This will cause the proxy to stop listening on `listen_host:listen_port` as well as stop sending to `upstream_host:upsream_port`

## Message

```json
{
    "operation": "stop",
    "param": nil,
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The proxy was successfully stopped.                    |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |


# Start

The proxy can be started by publishing a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with the operation `start`. This will cause the proxy to start listening on `listen_host:listen_port` as well as stop sending to `upstream_host:upsream_port`

## Message

```json
{
    "operation": "start",
    "param": nil,
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The proxy was successfully started.                    |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |


# Reset

The currently running models can be reset to their default state by publishing a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with an operation of `reset`. The modules will continue to run, however, any session state will be reset to the beginning of the session.

## Message

```json
{
    "operation": "reset",
    "param": nil,
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The modules were successfully reset.                   |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |


# Reload

The upstream address can be changed by publishing a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with an operation of `upstream_host`. This will cause the proxy to stop sending to the current address and then start sending to the new address given as a `param`.

## Message

```json
{
    "operation": "upstream_host",
    "param": "<ip_address/hostname>",
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The upstream host  was successfully set.               |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |


# Bind_host

The proxy service bind address can be changed by publishing a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with an operation of `bind_host`. This will cause the proxy service to stop listening on the current address and then start listening on the new address given as a `param`.

## Message

```json
{
    "operation": "bind_host",
    "param": "<ip_address/hostname>",
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The bind host was successfully changed.                |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |



# Bind_port

The proxy service bind port can be changed by publishing a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with an operation of `bind_port`. This will cause the proxy service to stop listening on the current port and then start listening on the new port given as a `param`.

## Message

```json
{
    "operation": "bind_port",
    "param": "<port number>",
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The request was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The bind port was successfully changed.                |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |


# Start_Recording

The proxy service will start recording proxy traffic when a `start_recording` interface operation message is published to the `proxy_mgmt_request` REDIS pubs channel. This will cause the proxy service to start recording traffic using the given recording_id in `param`. If the the proxy is already recording traffice, an error will be returned.

  ## Message

  ```json
  {
      "operation": "start_recording",
      "param": "<recording_id>",
      "key": string
  }
  ```
  ## Example Response

  ## Message

  ```json
  {
      "code": 200,
      "message": "The request was successful",
      "key": string
  }
  ```
  ### Response Codes

  | Status Code | Description                                                                        |
  |:------------|:-----------------------------------------------------------------------------------|
  | 200-299     | The request was successful. The bind port was successfully changed.                |
  | 400         | Bad request. Typically returned if required information was not provided as input. |
  | 500-599     | Server error.                                                                      |


# Stop_Recording

  The proxy service will stop recording proxy traffic when a `stop_recording` interface operation message is published to the `proxy_mgmt_request` REDIS pubs channel. This will cause the proxy service to stop recording traffic.

  ## Message

  ```json
  {
      "operation": "stop_recording",
      "param": "n/a",
      "key": string
  }
  ```
  ## Example Response

  ## Message

  ```json
  {
      "code": 200,
      "message": "The request was successful",
      "key": string
  }
  ```
  ### Response Codes

  | Status Code | Description                                                                        |
  |:------------|:-----------------------------------------------------------------------------------|
  | 200-299     | The request was successful. The bind port was successfully changed.                |
  | 400         | Bad request. Typically returned if required information was not provided as input. |
  | 500-599     | Server error.                                                                      |


# Status

The proxy service will return the current status of the proxy a `status` interface operation message is published to the `proxy_mgmt_request` REDIS pubs channel. This will cause the proxy service to query all of the currently running modules for status and aggregate them into a response or if a module name is given in `param`, then status for only the given module is returned

## Message

```json
{
    "operation": "status",
    "param": "<module_name>",
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message":
      {
        {
          "module": TrafficRecorder:
          "state": running,
          "status": 4/20/2015 8:00:00 am
        },
        {
          "module": FaultInjection:
          "state": Error,
          "status": "failed to load"
        },
        {
          "module": Latency:
          "state": stopped,
          "status": 4/20/2015 8:00:00 am
        }
      },
    "key": string
}
```

### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The bind port was successfully changed.                |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |

### States
| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| running     | The module is currently running. Status will indicate when it started running      |
| stopped     | The module is currently stopped. Implying it was once running. Status will indicate when it was stopped. |
| error       | The module stopped due to an error                                                 |
| loaded      | The module has been loaded, but not started.                                       |

# Test
Proxy test cases can be ran by sending publising a proxy interface operation message to the `proxy_mgmt_request` REDIS pubs channel with an operation of `test`. This will case the proxy service to run all configured tests or run the ttest provided as a `param`
## Message

```json
{
    "operation": "test",
    "param": "<test module name>",
    "key": string
}
```
## Example Response

## Message

```json
{
    "code": 200,
    "message": "The test was successful",
    "key": string
}
```
### Response Codes

| Status Code | Description                                                                        |
|:------------|:-----------------------------------------------------------------------------------|
| 200-299     | The request was successful. The test was successfully executed.                    |
| 400         | Bad request. Typically returned if required information was not provided as input. |
| 500-599     | Server error.                                                                      |
