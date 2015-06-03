- [QoS](#qos)
  - [Get a list of QoS profiles](#get-a-list-of-qos-profiles)
  - [Get QoS profile](#get-qos-profile)
  - [Create a new QoS profile](#create-a-new-qos-profile)
  - [Update QoS profile](#update-qos-profile)
  - [Delete QoS profile](#delete-qos-profile)

# Quality of Service Profile

## Get a list of QoS profiles

To retrieve a list of QoS profiles, an application submits an HTTP GET request to the URL that represents the QoS profile resource.

### Request

#### URL
`/qos`

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
| name | A string value that identifies the QoS profile. |
| description | A string value describing the QoS profile. |
| latency | A integer value that specifies latency in milliseconds. |
| jitter | A JSON containing "min" and "max" keys that specify jitter min/max integers in milliseconds. |
| trafficLoss | A decimal value that specifies traffic loss as a percentage(eg 0.01 == 1%) |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of QoS profiles are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
{   "qos_profiles": [
        {
            "_id": "0xdeadbeef",
            "latency": 100,
            "jitter": {
                "min": 30,
                "max": 50
            },
            "trafficLoss": 0.1
        },
        {
            "_id": "0xbeefbeef",
            "latency": 150,
            "jitter": {
                "min": 15,
                "max": 25
            },
            "trafficLoss": 0.5
        },
    ]
    
}
```

## Get QoS Profile

To retrieve information about a QoS profile, an application submits an HTTP GET request to the URL that represents the QoS profile resource.

### Request

#### URL
`/qos/:id`, for example, `/qos/0xdeadbeef` to retrieve information about a QoS profile with ID 0xdeadbeef.

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
| name | A string value that identifies the QoS profile. |
| description | A string value describing the QoS profile. |
| latency | A integer value that specifies latency in milliseconds. |
| jitter | A JSON containing "min" and "max" keys that specify jitter min/max integers in milliseconds. |
| trafficLoss | A decimal value that specifies traffic loss as a percentage(eg 0.01 == 1%) |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The QoS profile information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```json
{
    "_id": "0xdeadbeef",
    "latency": 100,
    "jitter": {
        "min": 30,
        "max": 50
    },
    "trafficLoss": 0.1
}
```

## Create a new QoS profile

An application can create a QoS profile by issuing an HTTP POST request to the URL of the QoS profile resource.

### Request

#### URL
`/qos/`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a QoS profile representation with the following elements:

| Element | Description |
|---|---|
| name | A string value that identifies the QoS profile. |
| description | (optional) A string value describing the QoS profile. |
| latency | A integer value that specifies latency in milliseconds. |
| jitter | A JSON containing "min" and "max" keys that specify jitter min/max integers in milliseconds. |
| trafficLoss | A decimal value that specifies traffic loss as a percentage(eg 0.01 == 1%) |

#### Request example

```json
{
    "latency": 100,
    "jitter": {
        "min": 30,
        "max": 50
    },
    "trafficLoss": 0.1
}
```
### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |
| Location | The location of the newly created QoS profile. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The QoS profile was successfully created. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 201 Created
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Location: http://api.heliosburn.com/qos/0xdeadbeef
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```



## Update QoS profile

An application can update a QoS profile by issuing an HTTP PUT request to the URL of the containing QoS profile resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the QoS profile. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/qos/:id`, for example, `/qos/0xdeadbeef` to update the QoS profile with ID 0xdeadbeef.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a QoS profile representation with the elements to be modified:

| Element | Description |
|---|---|
| name | A string value that identifies the QoS profile. |
| description | A string value describing the QoS profile. |
| latency | A integer value that specifies latency in milliseconds. |
| jitter | A JSON containing "min" and "max" keys that specify jitter min/max integers in milliseconds. |
| trafficLoss | A decimal value that specifies traffic loss as a percentage(eg 0.01 == 1%) |

#### Request example

```json
{
    "latency": 100,
    "jitter": {
        "min": 30,
        "max": 50
    },
    "trafficLoss": 0.1
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
| 200-299 | The request was successful. The QoS profile was successfully updated. |
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

## Delete QoS profile

An application can delete a QoS profile by issuing an HTTP DELETE request to the URL of the containing QoS profile resource.

### Request

#### URL
`/qos/:id`, for example, `/qos/0xdeadbeef` to delete the QoS profile with ID 0xdeadbeef.

#### Method
DELETE

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

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
| 200-299 | The request was successful. The QoS profile was successfully deleted. |
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
