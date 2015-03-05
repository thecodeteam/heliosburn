- [Test Plan](#test-plan)
  - [Get a list of Test Plans](#get-a-list-of-test-plans)
  - [Get Test Plan details](#get-test-plan-details)
  - [Create a new Test Plan](#create-a-new-test-plan)
  - [Update Test Plan details](#update-test-plan-details)
  - [Delete a Test Plan](#delete-a-test-plan)

  
# Test Plan

## Get a list of Test Plans

To retrieve a list of Test Plans, an application submits an HTTP GET request to the URL that represents the Test Plan resource.

### Request

#### URL
`/testplan`

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
| latencyEnabled | A boolean value that indicates whether the latency is enabled or not. |
| clientLatency | An integer value that specifies the client latency in milliseconds.  |
| serverLatency | An integer value that specifies the client latency in milliseconds.  |
| rules | An integer value that specifies the number of rules associated to the Test Plan. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of Test Plans are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
[
    {
        "id": "54edbcd9eb90892f5eed9129",
        "name": "Amazon S3 Test Plan",
        "description": "My test plan for Amazon S3...",
        "rules": 42,
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "latencyEnabled": true,
        "clientLatency": 100,
        "serverLatency": 0
    },
    {
        "id": "h34b5k3425kl45b2345b3245b",
        "name": "Test Plan for Swift",
        "description": "bla bla bla bla bla blaaaa...",
        "rules": 654,
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "latencyEnabled": true,
        "clientLatency": 100,
        "serverLatency": 0
    }
]
```

## Get Test Plan details

To retrieve information about a Test Plan, an application submits an HTTP GET request to the URL that represents the Test Plan resource.

### Request

#### URL
`/testplan/:id`, for example, `/testplan/54edbcd9eb90892f5eed9129`.

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
| createdAt | A dateTime value that specifies the date and time the Test Plan was created. |
| updatedAt | A dateTime value that specifies the date and time the Test Plan was last modified. |
| latencyEnabled | A boolean value that indicates whether the latency is enabled or not. |
| clientLatency | An integer value that specifies the client latency in milliseconds.  |
| serverLatency | An integer value that specifies the client latency in milliseconds.  |
| rules | An integer value that specifies the number of rules associated to the Test Plan. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Test Plan information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```json
    {
        "id": "54edbcd9eb90892f5eed9129",
        "name": "Amazon S3 Test Plan",
        "description": "My test plan for Amazon S3...",
        "rules": 42,
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "latencyEnabled": true,
        "clientLatency": 100,
        "serverLatency": 0
    }
```


## Create a new Test Plan

An application can create a Test Plan by issuing an HTTP POST request to the URL of the containing Test Plan resource

### Request

#### URL
`/testplan/`

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
| name | Name of the Test Plan. |
| description | Description of the Test Plan. |
| latencyEnabled | A boolean value that indicates whether the latency is enabled or not. |
| clientLatency | An integer value that specifies the client latency in milliseconds.  |
| serverLatency | An integer value that specifies the client latency in milliseconds.  |

#### Request example

```json
POST https://api.heliosburn.com/testplans/ HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Test Plan",
    "description": "My test plan for Amazon S3...",
    "latencyEnabled": true,
    "clientLatency": 100,
    "serverLatency": 0
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
| 200-299 | The request was successful. The Test Plan was successfully created. |
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


## Update Test Plan details

An application can update a Test Plan by issuing an HTTP PUT request to the URL of the containing Test Plan resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the Test Plan. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/testplan/:id`, for example, `/testplan/54edbcd9eb90892f5eed9129`.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Test Plan representation with the elements to be modified:

| Element | Description |
|---|---|
| name | Name of the Test Plan. |
| description | Description of the Test Plan. |
| latencyEnabled | A boolean value that indicates whether the latency is enabled or not. |
| clientLatency | An integer value that specifies the client latency in milliseconds.  |
| serverLatency | An integer value that specifies the client latency in milliseconds.  |

#### Request example

```json
PUT https://api.heliosburn.com/testplans/54edbcd9eb90892f5eed9129 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Test Plan",
    "description": "My test plan for Amazon S3...",
    "latencyEnabled": true,
    "clientLatency": 100,
    "serverLatency": 0
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
| 200-299 | The request was successful. The Test Plan was successfully updated. |
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


## Delete a Test Plan

An application can permanantly delete a Test Plan by issuing an HTTP DELETE request to the URL of the Test Plan resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL
`/testplan/:id`, for example, `/testplan/54edbcd9eb90892f5eed9129`.

#### Method
DELETE

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Test Plan representation with the elements to be modified:

| Element | Description |
|---|---|
| name | Name of the session. |
| description | Description of the session. |
| latencyEnabled | A boolean value that indicates whether the latency is enabled or not. |
| clientLatency | An integer value that specifies the client latency in milliseconds.  |
| serverLatency | An integer value that specifies the client latency in milliseconds.  |

#### Request example

```
DELETE https://api.heliosburn.com/testplans/54edbcd9eb90892f5eed9129 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 0
Content-Type: application/json; charset=UTF-8
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
| 200-299 | The request was successful. The Test Plan was successfully deleted. |
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
