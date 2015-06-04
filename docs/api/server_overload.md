- [Server Overload Profiles](#server-overload-profile)
  - [Get a list of profiles](#get-a-list-of-profiles)
  - [Get profile](#get-profile)
  - [Create a new profile](#create-a-new-profile)
  - [Update profile](#update-profile)
  - [Delete profile](#delete-profile)

# Server Overload Profile

## Get a list of profiles

To retrieve a list of Server Overload profiles, an application submits an HTTP GET request to the URL that represents the profile resource.

### Request

#### URL
`/serveroverload`

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
| TODO | TODO |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of profiles are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
{   
   todo    
}
```

## Get Profile

To retrieve information about a profile, an application submits an HTTP GET request to the URL that represents the profile resource.

### Request

#### URL
`/serveroverload/:id`, for example, `/serveroverload/0xdeadbeef` to retrieve information about a profile with ID 0xdeadbeef.

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
| TODO| TODO |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The profile information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```json
{
    "name": "Raspberry PI Overload profile",
    "description": "bla bla...",
    "function": {
        "type": "exponential",
        "expValue": "3",
        "growthRate": "3"
    },
    "response_triggers": [
        {
            "fromLoad": 70,
            "toLoad": 80,
            "actions": [
                {
                    "type": "response",
                    "value": "503",
                    "percentage": 30
                },
                {
                    "type": "delay",
                    "value": "300",
                    "percentage": 100
                }
            ]
        },
        {
            "fromLoad": 80,
            "toLoad": null,
            "actions": [
                {
                    "type": "response",
                    "value": "503",
                    "percentage": 100
                }
            ]
        }
    ]
}
```

## Create a new profile

An application can create a profile by issuing an HTTP POST request to the URL of the profile resource.

### Request

#### URL
`/serveroverload/`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a profile representation with the following elements:

| Element | Description |
|---|---|
| TODO | TODO |
#### Request example

```json
{
    TODO
}
```
### Response

#### Response Header
The response header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the content. |
| Location | The location of the newly created profile. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The profile was successfully created. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 201 Created
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Location: http://api.heliosburn.com/serveroverload/0xdeadbeef
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```



## Update profile

An application can update a profile by issuing an HTTP PUT request to the URL of the containing profile resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the profile. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/profile/:id`, for example, `/profile/0xdeadbeef` to update the profile with ID 0xdeadbeef.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a profile representation with the elements to be modified:

| Element | Description |
|---|---|
| TODO | TODO |

#### Request example

```json
{
    TODO
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
| 200-299 | The request was successful. The profile was successfully updated. |
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

## Delete profile

An application can delete a profile by issuing an HTTP DELETE request to the URL of the containing profile resource.

### Request

#### URL
`/serveroverload/:id`, for example, `/serveroverload/0xdeadbeef` to delete the profile with ID 0xdeadbeef.

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
| 200-299 | The request was successful. The profile was successfully deleted. |
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
