- [Session](#session)
  - [Get a list of Sessions](#get-a-list-of-sessions)
  - [Get Session details](#get-session-details)
  - [Create a new Session](#create-a-new-session)
  - [Update Session details](#update-session-details)
  - [Run a Session](#run-a-session)
  - [Stop a running Session](#stop-a-running-session)

# Session

## Get a list of Sessions

To retrieve a list of sessions, an application submits an HTTP GET request to the URL that represents the session resource.

### Request

#### URL
`/session`

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

The response body contains a list containing the following elements in JSON format:

| Element | Description |
|---|---|
| id | An integer value that uniquely identifies the session. |
| name | Name of the session. |
| description | Description of the session. |
| upstreamHost | The upstream host or IP of the HTTP server to test. |
| upstreamPort | The upstream port number of the HTTP server to test. |
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| testPlan | Test Plan JSON representation. Refer to the Test Plan resource documentation. |
| user | User JSON representation. Refer to the User resource documentation. |
| executions | An integer value that specifies the number of times the session has been executed. |
| qosProfile | The ID of a QoS profile . |
| serverOverloadProfile | The ID of a Server Overload profile. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of sessions are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
[
    {
        "id": 1,
        "name": "Session A",
        "description": "This is a description for a Session",
        "upstreamHost": "github.com",
        "upstreamPort": 80,
        "qosProfile": "0xdeadbeef",
        "serverOverloadProfile": "0xfedbeef",

        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "testPlan":
            {
                "id": 12,
                "name": "ViPR Test plan"
            },
	    "user":
    	    {
                "id": 1,
                "username": "John Doe"
            },
        "executions": 42,
        "latest_execution_at": "2014-02-12 03:34:51"
    },
    {
        "id": 2,
        "name": "ViPR Session 1",
        "upstreamHost": "github.com",
        "upstreamPort": 80,
        "qosProfile": "0xdeadbeef",
        "serverOverloadProfile": "0xfedbeef",

        "description": "This is a description for a Session",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "testPlan":
            {
                "id": 12,
                "name": "ViPR Test plan"
            },
	    "user":
    	    {
                "id": 1,
                "username": "John Doe"
            },
        "executions": 634,
        "latest_execution_at": "2014-02-12 03:34:51"
    }
]
```

## Get Session details

To retrieve information about a Session, an application submits an HTTP GET request to the URL that represents the Session resource.

### Request

#### URL
`/session/:id`, for example, `/session/23` to retrieve information about a Session with ID 23.

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

The response body contains the following elements in JSON format:

| Element | Description |
|---|---|
| id | An integer value that uniquely identifies the session. |
| name | Name of the session. |
| description | Description of the session. |
| upstreamHost | The upstream host or IP of the HTTP server to test. |
| upstreamPort | The upstream port number of the HTTP server to test. |
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| testPlan | Test Plan JSON representation. Refer to the Test Plan resource documentation. |
| user | User JSON representation. Refer to the User resource documentation. |
| executions | An integer value that specifies the number of times the session has been executed. |
| qosProfile | The ID of a QoS profile . |
| serverOverloadProfile | The ID of a Server Overload profile. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The session information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```json

    {
        "id": 1,
        "name": "Session A",
        "description": "This is a description for a Session",
        "upstreamHost": "github.com",
        "upstreamPort": 80,
        "qosProfile": "0xdeadbeef",
        "serverOverloadProfile": "0xfedbeef",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "testPlan":
            {
                "id": 12,
                "name": "ViPR Test plan"
            },
	    "user":
    	    {
                "id": 1,
                "username": "John Doe"
            },
        "executions": 42,
    }
```

## Create a new Session

An application can create a Session by issuing an HTTP POST request to the URL of the containing Session resource

### Request

#### URL
`/session/`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Session representation with the following elements:

| Element | Description |
|---|---|
| name | Name of the session. |
| description | Description of the session. |
| testPlan | Optional. Test Plan JSON representation containing only the ID. |
| upstreamHost | The upstream host or IP of the HTTP server to test. |
| upstreamPort | The upstream port number of the HTTP server to test. |
| qosProfile | The ID of a QoS profile . |
| serverOverloadProfile | The ID of a Server Overload profile. |


#### Request example

```
POST https://api.heliosburn.com/testplans/ HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Session",
    "description": "My session for Amazon S3...",
    "upstreamHost": "github.com",
    "upstreamPort": 80,
    "qosProfile": "0xdeadbeef",
    "serverOverloadProfile": "0xfedbeef",
    "testPlan":
        {
            "id": 12,
        }
}
```
### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |
| Location | The location of the newly created Session. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Session was successfully created. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 201 Created
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Location: http://api.heliosburn.com/testplans/65
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```



## Update Session details

An application can update a Session by issuing an HTTP PUT request to the URL of the containing Session resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the Session. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/session/:id`, for example, `/session/23` to update the Session with ID 23.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Session representation with the elements to be modified:

| Element | Description |
|---|---|
| name | Name of the session. |
| description | Description of the session. |
| testPlan | Test Plan JSON representation containing only the ID. |
| qosProfile | The ID of a QoS profile . |
| serverOverloadProfile | The ID of a Server Overload profile. |

#### Request example

```
PUT https://api.heliosburn.com/testplans/34 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Session",
    "description": "My session for Amazon S3...",
    "testPlan":
    {
        "id": 12
    }
}
```
### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Session was successfully updated. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```




## Run a Session

An application can run a Session by issuing an HTTP POST request to the URL that represents the start of a Session.

### Request

#### URL
`/session/:id/start`, for example, `/session/23/start` to start the Session with ID 23.

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains the parameters for the Session execution.

| Element | Description |
|---|---|
| stopAfter | Integer value that specifies the number of minutes after which the Session will stop. If this parameter is not set, the Session will run indefinitely until it is explicitly stopped. |

#### Request example

```
POST https://api.heliosburn.com/session/23/start HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "stopAfter": 60
}
```

### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Session was successfully started. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 409 | Conflict. HeliosBurn cannot start the Session due to a conflict. Another Session may be running already. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```


## Stop a running Session

An application can stop a running Session by issuing an HTTP POST request to the URL that represents the stop of a Session.

### Request

#### URL
`/session/:id/stop`, for example, `/session/23/stop`.

#### Method
POST

#### Request example

```
POST https://api.heliosburn.com/session/23/stop HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 0
```
### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |

#### Response Body

JSON input that contains the following elements.

| Element | Description |
|---|---|
| id | An integer value that uniquely identifies the Session execution. |
| sessionId | An integer value that uniquely identifies the Session. |
| startedAt | A dateTime value that specifies the date and time the Session was started. |
| stoppedAt | A dateTime value that specifies the date and time the Session was stopped. |
| requests | An integer value containing the number of requests processed during the execution. |
| matches | An integer value containing the number of requests that matched a rule. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Session was successfully stopped. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 409 | Conflict. HeliosBurn cannot stop the Session due to a conflict. The Session may not be running. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 213
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5

{
    "id": 32,
    "sessionId": 18,
    "startedAt": "2014-02-12 03:34:51",
    "stoppedAt": "2014-02-12 03:54:33",
    "requests": 841,
    "matches": 320
}
```
