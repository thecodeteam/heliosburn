- [Recording](#recording)
  - [Create a Recording](#create-a-recording)
  - [Get a list of Recordings](#get-a-list-of-recordings)
  - [Get Recording details](#get-recording-details)
  - [Update a Recording](#update-a-recording)
  - [Delete a Recording](#delete-a-recording)
  - [Start a recording](#start-a-recording)
  - [Stop a recording](#stop-a-recording)


# Recording

A recording is a set of HTTP traffic of a particular period of time. It can be useful to analize the requests and responses to, afterwards, generate rules out of them. Those rules will be used as a baseline to edit them with the preferred actions. A recording can only be started if the proxy is idle (e.g. not doing any other recording or running a session).



## Create a Recording

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
    "description": "Endpoint test #1"
}
```

### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |
| Location | The location of the newly created Recording. |

#### Response Body
The response body is a JSON containing the id of the created recording.

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

{"id": "0xdeadbeef"}
```


## Get a list of Recordings

To retrieve a list of Recordings, an application submits an HTTP GET request to the URL that represents the Recording resource.

### Request

#### URL
`/recording`

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
| id | An alphanumeric value that uniquely identifies the Test Plan. |
| name | Name of the Test Plan. |
| description | Description of the Test Plan. |
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| count | An integer value that specifies the number of transactions associated to the Recording. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of Recordings is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
[
    {
        "id": "54edbcd9eb90892f5eed9129",
        "name": "Recording of Swift traffic",
        "description": "bla bla bla bla...",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "count": 451
    },
    {
        "id": "54edbcd9eb90892f5eed9129",
        "name": "Recording of Swift traffic",
        "description": "bla bla bla bla...",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "count": 451
    }
]
```


## Get Recording details

To retrieve information about a Recording, an application submits an HTTP GET request to the URL that represents the Recording resource. If a recording
contains a large amount of traffic, you may wish to receive it in chunks rather than a single massive response.

### Request

#### URL
`/recording/:id`, for example, `/recording/54edbcd9eb90892f5eed9129`.

#### URL to receive traffic in chunks
`/recording/:id?traffic_begin=:n&traffic_end=:n`, for example, `/recording/:id?traffic_begin=0&traffic_end=500`

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
| id | An alphanumeric value that uniquely identifies the Test Plan. |
| name | Name of the Test Plan. |
| description | Description of the Test Plan. |
| createdAt | A dateTime value that specifies the date and time the recording was created. |
| updatedAt | A dateTime value that specifies the date and time the recording was last modified. |
| startedAt | A dateTime value that specifies the date and time the recording was started. |
| stoppedAt | A dateTime value that specifies the date and time the recording was stopped. |
| count | An integer value that specifies the number of transactions associated to the Recording. |

#### Response query string variables
| Query variable | Description |
|---|---|
| traffic_begin | (OPTIONAL) An integer of the first piece of traffic to return. The lowest value is 0. |
| traffic_begin | (OPTIONAL) An integer of the last piece of traffic to return. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Recording information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```json
{
    "id": "54edbcd9eb90892f5eed9129",
    "name": "Recording of Swift traffic",
    "description": "bla bla bla bla...",
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:56:01",
    "startedAt": "2014-02-12 03:35:23",
    "stoppedAt": "2014-02-12 03:56:01",
    "count": 601229
    "traffic" [
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      { <Traffic Object> },
      ...
    ]
}
```


## Update a Recording

An application can update a Recording by issuing an HTTP PUT request to the URL of the containing Recording resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the Recording. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/recording/:id`, for example, `/recording/54edbcd9eb90892f5eed9129`.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Recording representation with the elements to be modified:

| Element | Description |
|---|---|
| name | Name of the Recording. |
| description | Description of the Recording. |

#### Request example

```json
PUT https://api.heliosburn.com/recording/54edbcd9eb90892f5eed9129 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Updated recording name",
    "description": "A more descriptive name for this recording."
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
| 200-299 | The request was successful. The Recording was successfully updated. |
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


## Delete a Recording

An application can permanently delete a Recording by issuing an HTTP DELETE request to the URL of the Recording resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL
`/recording/:id`, for example, `/recording/54edbcd9eb90892f5eed9129`.

#### Method
DELETE

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |


#### Request example

```
DELETE https://api.heliosburn.com/recording/54edbcd9eb90892f5eed9129 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 0
Content-Type: application/json; charset=UTF-8
```

### Response

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Recording was successfully deleted. |
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




## Start a recording

To start a recording an application must issue a HTTP POST request to the URL that represents the Recording.

### Request

#### URL
`/recording/:recording_id/start`, for example, `/recording/12345/start`.

#### Method
POST


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





## Stop a Recording

An application can stop a running Recording by issuing an HTTP POST request to the URL that represents the stop of a Session.

### Request

#### URL
`/recording/:id/stop`, for example, `/recording/23/stop`.

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
