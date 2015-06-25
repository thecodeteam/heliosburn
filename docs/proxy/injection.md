- [Injection Module](#injection-module)
  - [Injection Engine](#injection-engine)



# Injection Module

The injection module is situated inside the proxy processing pipeline as the last module to process a request or a response. When the module receives a response or request, the corresponding metadata is passed to the injection engine for analysis. The injection engine then provides to the module the `action` component of the `rule` database or `None` if no rule matches.

  ![alt text](../figures/HB_Injection.png "Injecting HTTP Metadata")



## Injection Actions

The following possible actions are implemented as command objects and executed if the corresponding action type is returned by the injection engine:

| Action      | Context | Description                                                                                                                                                                                                              |
|:------------|:--------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| modify      | both    | Modifies different aspects of a given request or response.                                                                                                                                                               |
| newResponse | both    | Generates a completely new response independently of the given request or response. Note that if used in the `request` context it will directly respond to the client without even forwarding the request to the server. |
| newRequest  | request | Generates a completely new request independently of the given request.                                                                                                                                                   |
| drop        | both    | Drops the HTTP connection.                                                                                                                                                                                               |
| reset       | both    | Resets the HTTP connection.                                                                                                                                                                                              |

## Injection Engine
Given a request or response the injection engine will retun an action response. That response will then be used to determine what action the injection module will apply.

### Modify Action
An action type `modify` contains the following elements depending on the traffic context.

### Injection engine response

```json
"action": {
    "type": "modify",
    "method": "PUT",
    "setHeaders": [
        {
            "key": "X-Auth-Token",
            "value": "k54l3b6k6b43l56b346"
        }
    ],
    "deleteHeaders": [
        {
            "key": "User-Agent"
        }
    ]
}
```

| Element           | Context  | Description                                                 |
|:------------------|:---------|:------------------------------------------------------------|
| httpProtocol      | both     | HTTP protocol.                                              |
| method            | request  | Request method.                                             |
| url               | request  | Request URL.                                                |
| statusCode        | response | Status Code.                                                |
| statusDescription | response | Status description.                                         |
| setHeaders        | both     | List of headers to be set to the request or response.       |
| deleteHeaders     | both     | List of headers to be deleted from the request or response. |


## NewResponseAction

An action type `newResponse` contains the following elements.

### Injection engine response

```json
"action": {
    "type": "newResponse",
    "httpProtocol": "HTTP/1.1",
    "statusCode": 400,
    "statusDescription": "Bad Request"
    "headers": [
        {
            "key": "E-Tag",
            "value": "9384253245"
        },
        {
            "key": "Server",
            "value": "HeliosBurn"
        }
    ],
    "payload": "Intercepted by HeliosBurn"
}
```

| Element           | Description         |
|:------------------|:--------------------|
| httpProtocol      | HTTP protocol.      |
| statusCode        | Status Code.        |
| statusDescription | Status description. |
| headers           | List of headers.    |
| payload           | Response payload.   |


## NewRequestAction

An action type `newRequest` contains the following elements.

| Element      | Description      |
|:-------------|:-----------------|
| httpProtocol | HTTP protocol.   |
| method       | Request method.  |
| url          | Request URL.     |
| headers      | List of headers. |
| payload      | Request payload. |

## dropAction

The action type `drop` has no elements

### Injection Engine Response
```json
"action": {
    "type": "drop",
}
```

## resetAction

The action type `reset` has no elements

### Injection engine response
```json
"action": {
    "type": "reset",
}
```

# Metric Collection

The injection module will continuously update a set of metrics that may be useful in future analysis of the injection session. Each metrics is available in real-time by making the module `status` API call. The following metrics are collected:

| metric        | Description                                      |
|:--------------|:-------------------------------------------------|
| modified      | The current number of modified request/responses |
| new_Responses | The current count of new responses sent          |
| new_requests  | The current total number of new requests sent    |
| dropped       | The current count of dropped connections         |
| reset         | The current count of reset connections           |
