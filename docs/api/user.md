- [User](#user)
  - [Get a list of Users](#get-a-list-of-users)
  - [Get User details](#get-user-details)
  - [Create a new User](#create-a-new-user)
  - [Update User details](#update-user-details)
  - [Delete a User](#delete-a-user)


# User

## Get a list of Users

To retrieve a list of Users, an application submits an HTTP GET request to the URL that represents the User resource.

### Request

#### URL
`/user`

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
| username | Name of the User. |
| email | Email of the User. |
| createdAt | A dateTime value that specifies the date and time the User was created. |
| updatedAt | A dateTime value that specifies the date and time the User was last modified. |
| sessions | An integer value that specifies the number of sessions belonging to the User. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of Users are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Date: Fri, 22 Oct 2014 08:01:54 GMT
Server: Noelios-Restlet-Engine/1.1.5
[
    {
        "username": "johndoe",
        "email": "john.doe@example.com",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "sessions": 34
    },
    {
        "username": "janedoe",
        "email": "jane.doe@example.com",
        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "sessions": 9
    }
]
```

## Get User details

To retrieve information about a User, an application submits an HTTP GET request to the URL that represents the User resource.

### Request

#### URL
`/user/:username`, for example, `/user/johndoe` to retrieve information about a User with username "johndoe".

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
| username | Name of the User. |
| email | Email of the User. |
| createdAt | A dateTime value that specifies the date and time the User was created. |
| updatedAt | A dateTime value that specifies the date and time the User was last modified. |
| sessions | A list of Session JSON representation. Refer to the Session resource documentation. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The User information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response example

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Date: Fri, 22 Oct 2014 08:01:54 GMT
Server: Noelios-Restlet-Engine/1.1.5
{
    "username": "janedoe",
    "email": "jane.doe@example.com",
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:51",
    "sessions":
        [
            {
                "id": 1,
                "name": "Session A",
                "description": "This is a description for a Session",
                "createdAt": "2014-02-12 03:34:51",
                "updatedAt": "2014-02-12 03:34:51",
                "testPlan":
                    {
                        "id": 12,
                        "name": "ViPR Test plan"
                    },
                "executions": 42,
                "latest_execution_at": "2014-02-12 03:34:51"
            },
            {
                "id": 2,
                "name": "ViPR Session 1",
                "description": "This is a description for a Session",
                "createdAt": "2014-02-12 03:34:51",
                "updatedAt": "2014-02-12 03:34:51",
                "testPlan":
                    {
                        "id": 12,
                        "name": "ViPR Test plan"
                    },
                "executions": 634,
                "latest_execution_at": "2014-02-12 03:34:51"
            }
        ]
}
```

## Create a new User

An application can create a User by issuing an HTTP POST request to the URL of the containing User resource

### Request

#### URL
`/user/`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a User representation with the following elements:

| Element | Description |
|---|---|
| username | Username. |
| email | Email of the User. |
| password | Password of the User |

#### Request example

```
POST https://api.heliosburn.com/user/ HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "Super secure password"
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
Location: http://api.heliosburn.com/user/johndoe
Server: Noelios-Restlet-Engine/1.1.5
```

## Update User details

An application can update a User by issuing an HTTP PUT request to the URL of the containing User resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the User. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/user/:username`, for example, `/user/johndoe` to update the User with username "johndoe".

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a User representation with the elements to be modified:

| Element | Description |
|---|---|
| email | Email of the User. |
| password | Password of the User |

#### Request example

```
PUT https://api.heliosburn.com/user/johndoe HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "email": "johndoe@example.com",
    "password": "Super secure password"
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


## Delete a User

An application can permanently delete a User by issuing an HTTP DELETE request to the URL of the User resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL
`/user/:username`, for example, `/user/johndoe` to delete the User with username "johndoe".

#### Method
DELETE


#### Request example

```
DELETE https://api.heliosburn.com/user/johndoe HTTP/1.1
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
| 200-299 | The request was successful. The User was successfully deleted. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 404 | Not found. The resource was not found. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 204 No Content
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5
```
