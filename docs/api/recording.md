- [Recording](#recording)
  - [Start a new recording](#start-a-new-recording)
  - [Stop a recording](#stop-a-recording)


# Recording

A recording is a set of HTTP traffic of a particular period of time. It can be useful to analize the requests and responses to, afterwards, generate rules out of them. Those rules will be used as a baseline to edit them with the preferred actions. A recording can only be started if the proxy is idle (e.g. not doing any other recording or running a session).



## Create a new Recording

An application can create a Recording by issuing an HTTP POST request to the URL of the containing Recording resource. Note that creating a recording does automatically start it. To start a recording see the appropriate action.

### Request

#### URL
`/recording/`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Test Plan representation with the following elements:

| Element | Description |
|---|---|
| name | Name of the recording. |
| description | Description of the recording. |

#### Request example

```
POST https://api.heliosburn.com/recording/ HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "My Recording",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
}
```

### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |
| Location | The location of the newly created Test Plan. |

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
Location: http://api.heliosburn.com/recording/123
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```



## Start a recording

To start a recording an application must issue a HTTP POST request to the URL that represents the Recording.

### Request

#### URL
`/recording/:recording_id/start`, for example, `/recording/12345/start`.

#### Method
POST

####

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
| 409 | Conflict. HeliosBurn cannot start the Recording due to a conflict. Another Session or Recording may be running already. |
| 500-599 | Server error. |


#### Response Body

The response body will not contain anything if the request was processed successfully.

If the returned status code is `409 Conflict`, the response body will contain the following elements in JSON format:

| Element | Description |
|---|---|
| status | Status of the proxy server. It can either be `idle` or `busy`. It should be `busy` since the proxy could start the recording. |

If the `status` element is `busy`, the response body will also contain the following elements:

| Element | Description |
|---|---|
| busySince | A dateTime value that specifies the date and time since the proxy server has been busy. |
| busyWith | The URL of the resource that is running in the server, so that the user can stop or get more information about the execution. |


#### Response Example

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```

Response if HeliosBurn was already running another resource:

```
HTTP/1.1 409 Conflict
Content-Type: application/json; charset=UTF-8
Content-Length: 20
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5

{
    "status": "busy",
    "busySince": "2014-02-12 03:34:51",
    "busyWith": "http://api.heliosburn.com/session/23"
}
```
