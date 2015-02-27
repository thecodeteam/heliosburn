
**List of resources**

- [Authentication](#authentication)
  - [Login](#login)
- [User](#user)
  - [Get a list of Users](#get-a-list-of-users)
  - [Get User details](#get-user-details)
  - [Create a new User](#create-a-new-user)
  - [Update User details](#update-user-details)
  - [Delete a User](#delete-a-user)
- [Session](#session)
  - [Get a list of Sessions](#get-a-list-of-sessions)
  - [Get Session details](#get-session-details)
  - [Create a new Session](#create-a-new-session)
  - [Update Session details](#update-session-details)
- [Test Plan](#test-plan)
  - [Get a list of Test Plans](#get-a-list-of-test-plans)
  - [Get Test Plan details](#get-test-plan-details)
  - [Create a new Test Plan](#create-a-new-test-plan)
  - [Update Test Plan details](#update-test-plan-details)
  - [Delete a Test Plan](#delete-a-test-plan)
- [Rule](#rule)
  - [Get a list of Rules](#get-a-list-of-rules)
  - [Get Rule details](#get-rule-details)
  - [Create a new Rule](#create-a-new-rule)
  - [Update Rule details](#update-rule-details)
  - [Delete a Rule](#delete-a-rule)
- [Recording](#recording)
  - [Start a new recording](#start-a-new-recording)
  - [Stop a recording](#stop-a-recording)
- [Actions](#actions)
  - [Run a Session](#run-a-session)
  - [Stop a running Session](#stop-a-running-session)
  - [Get the proxy status](#get-the-proxy-status)
  - [Get current traffic](#get-current-traffic)



# Authentication

## Login

An application can authenticate a user by issuing an HTTP POST request to the URL of the containing Authentication resource.

### Request

#### URL
`/auth/login`

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
| password | Password of the User. |

#### Request example

```
POST https://api.heliosburn.com/auth/login HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "username": "johndoe",
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
| X-Auth-Token | The authentication token that will be sent in all subsequent calls. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Session was successfully created. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response Example

Authenticated successfully:
```
HTTP/1.1 200 OK
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
X-Auth-Token: 34hj2bkj45bkj3425v3jk245v3k5
Server: Noelios-Restlet-Engine/1.1.5
```

Invalid login credentials:

```
HTTP/1.1 401 Unauthorized
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Server: Noelios-Restlet-Engine/1.1.5
```



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
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| testPlan | Test Plan JSON representation. Refer to the Test Plan resource documentation. |
| user | User JSON representation. Refer to the User resource documentation. |
| executions | An integer value that specifies the number of times the session has been executed. |

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
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| testPlan | Test Plan JSON representation. Refer to the Test Plan resource documentation. |
| user | User JSON representation. Refer to the User resource documentation. |
| executions | An integer value that specifies the number of times the session has been executed. |

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

JSON input that contains a Test Plan representation with the following elements:

| Element | Description |
|---|---|
| name | Name of the session. |
| description | Description of the session. |
| testPlan | Optional. Test Plan JSON representation containing only the ID. |

#### Request example

```
POST https://api.heliosburn.com/testplans/ HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Test Plan",
    "description": "My test plan for Amazon S3...",
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

JSON input that contains a Test Plan representation with the elements to be modified:

| Element | Description |
|---|---|
| name | Name of the session. |
| description | Description of the session. |
| testPlan | Test Plan JSON representation containing only the ID. |

#### Request example

```
PUT https://api.heliosburn.com/testplans/34 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "name": "Amazon S3 Test Plan",
    "description": "My test plan for Amazon S3...",
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







# Rule

Rules will determine how the traffic is altered and, therefore, they are the most important part of the traffic injection engine. Rules can be either `request` or `response` types, the type determines when the rule is applied in the whole process. `request` rules are evaluated when HeliosBurn receives an HTTP request from the client and before forwarding it to the server. Whereas `response` rules are evaluated once HeliosBurn has received the response from the server and before forwarding it to the client.

A rule is made up of an `filter` and a `action`.

The filter determines whether or not the rule matches a given request or response. A filter includes information about the different aspects of HTTP traffic that will be used to compare it with the real traffic. Filter elements vary depending on the type of rule (i.e. `request` or `response`).

The following table shows the different kind of elements that can be specified in a filter and in which context (i.e. rule type) they are applied.

| Filter | Context | Description |
|---|---|---|
| httpProtocol | both | Text that will be compared to the request or response HTTP protocol. |
| method | both | Text that will be compared to the request method. |
| url | both | Text that will be compared to the request URL. |
| statusCode | response | Integer to be compared with the status code returned by the server. |
| headers | both | List of header filters to be compared to the HTTP headers in the request or response. A header filter can contain either only the header key or both the header key and value. If it only contains the header key, only the key will be compared to the given headers. If it contains both the key and the value, both elements will be compared. |

> **Note**: All text filters are evaluated using regular expressions.

The action determines how the given request or response is altered. An action is only applied if the filter fully matches the evaluated request or response. Actions vary depending on the type of rule (i.e. `request` or `response`).

The following table shows the different kind of actions available and in which context (i.e. rule type) they are applied.

| Action | Context | Description |
|---|---|---|
| modify | both | Modifies different aspects of a given request or response. |
| newResponse | both | Generates a completely new response independently of the given request or response. Note that if used in the `request` context it will directly respond to the client without even forwarding the request to the server. |
| newRequest | request | Generates a completely new request independently of the given request. |
| drop | both | Drops the HTTP connection. | 
| reset | both | Resets the HTTP connection. |


An action type `modify` contains the following elements depending on the traffic context.

| Element | Context | Description |
|---|---|---|
| httpProtocol | both | HTTP protocol. |
| method | request | Request method. |
| url | request | Request URL. |
| statusCode | response | Status Code. |
| statusDescription | response | Status description. |
| setHeaders | both | List of headers to be set to the request or response. |
| deleteHeaders | both | List of headers to be deleted from the request or response. |

An action type `newResponse` contains the following elements.

| Element | Description |
|---|---|
| httpProtocol | HTTP protocol. |
| statusCode | Status Code. |
| statusDescription | Status description. |
| headers | List of headers. |
| payload | Response payload. |

An action type `newRequest` contains the following elements.

| Element | Description |
|---|---|
| httpProtocol | HTTP protocol. |
| method | Request method. |
| url | Request URL. |
| headers | List of headers. |
| payload | Request payload. |

Action types `drop` and `reset` do not contain any elements.


The following example will modify all requests that use an HTTP protocol `HTTP/1.1`, have the HTTP method `GET`, contain the header `X-Auth-Token`, and have the header `User-Agent` with value `Mozilla`. If a request matches the filter, it will be modified by changing the HTTP method to `PUT`, updating the `X-Auth-Token` value to `k54l3b6k6b43l56b346`, and deleting the header `User-Agent`, if present.

```json
{
    "id": "32j45kbk3245b3245kbn",
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:52",
    "ruleType": "request",
    "testplanId": "k980ufd9g34kbwejv243v5342",
    "filter": {
        "httpProtocol": "HTTP/1.1",
        "method": "GET",
        "headers": [
            {
                "key": "X-Auth-Token"
            },
            {
                "key": "User-Agent",
                "value": "Mozilla"
            }
        ]
    },
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
}
```

The next example will intercept all requests to the URL "http://example.com/foo/bas", independently of the method used, and immediately respond with a "400 Bad Request" response containing two headers and a custom payload. Note that the server will not even receive the request.


```json
{
    "id": "32j45kbk3245b3245kbn",
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:52",
    "ruleType": "request",
    "testplanId": "k980ufd9g34kbwejv243v5342",
    "filter": {
        "url": "http://example.com/foo/bas"
    },
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
}
```


The rule below is applied at the "response" context (i.e. after receiving the response from the server and before forwarding it to the client). The rule activates when receiving a `200 OK` response from the server to a PUT request to the URL "http://example.com/foo/bar". If the filter matches the request and response, HeliosBurn will change the status code to `500 Internal Server Error` and set two additional headers.

```json
{
    "id": "32j45kbk3245b3245kbn",
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:52",
    "ruleType": "response",
    "testplanId": "k980ufd9g34kbwejv243v5342",
    "filter": {
        "statusCode": 200,
        "method": "PUT",
        "url": "http://example.com/foo/bar"
    },
    "action": {
        "type": "modify",
        "statusCode": 500,
        "statusDescription": "Internal Server Error"
        "setHeaders": [
            {
                "key": "E-Tag",
                "value": "9384253245"
            },
            {
                "key": "Server",
                "value": "HeliosBurn"
            }
        ]
    }
}
```


## Get a list of Rules in a Test Plan

To retrieve a list of Test Plan Rules, an application submits an HTTP GET request to the URL that represents the Rule resource for a Test Plan.

### Request

#### URL
`/testplan/:testplan_id/rule/`

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

The response body contains a `rules` key containing a list with the following elements in JSON format:

| Element | Description |
|---|---|
| id | An alphanumeric value that uniquely identifies the Rule. |
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| ruleType | A string value that specifies `request` or `response`.|
| testplanId | An ID identifying the testplan_id a Rule belongs to. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The list of Test Plans are in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

```json
{
    "rules": [
        {
            "id": "32j45kbk3245b3245kbn",
            "createdAt": "2014-02-12 03:34:51",
            "updatedAt": "2014-02-12 03:34:52",
            "ruleType": "request",
            "testplanId": "k980ufd9g34kbwejv243v5342",
            "filter": {
                "method": "GET",
                "headers": [
                    {
                        "key": "X-Auth-Token"
                    },
                    {
                        "key": "User-Agent",
                        "value": "Mozilla"
                    }
                ]
            },
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
       },
       {
            "id": "j34k2b5l3425bl3425l03",
            "createdAt": "2014-02-12 03:34:51",
            "updatedAt": "2014-02-12 03:34:52",
            "ruleType": "response",
            "testplanId": "91ho4ilqebhdib34kre",
            "filter": {
                "statusCode": 200
            },
            "action": {
                "type": "modify",
                "statusCode": 404
            }
        }
    ]
}
```

## Get Rule details

To retrieve information about a Rule, an application submits an HTTP GET request to the URL that represents the Rule's resource.

### Request

#### URL
`/testplan/:testplan_id/rule/:rule_id`, for example, `/testplan/89345hb342hb5bdfsg3/rule/j34k2b5l3425bl3425l03`.

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
| id | An alphanumeric value that uniquely identifies the Rule. |
| createdAt | A dateTime value that specifies the date and time the session was created. |
| updatedAt | A dateTime value that specifies the date and time the session was last modified. |
| ruleType | A string value that specifies `request` or `response`.|
| testplanId | An ID identifying the testplan_id a rule belongs to. |
| filter | The filter that will be applied to determine whether or not the rule matches a given request or response. See the `Filter` resource. |
| action | The action that will be applied when the filter matches the given request or response. |

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
   	"id": "j34k2b5l3425bl3425l03",
	"createdAt": "2014-02-12 03:34:51",
	"updatedAt": "2014-02-12 03:34:52",
	"ruleType": "request",
	"testplanId": "j34k2b5l3425bl3425l03",
    "filter": {
        "method": "GET",
        "headers": [
            {
                "key": "X-Auth-Token"
            },
            {
                "key": "User-Agent",
                "value": "Mozilla"
            }
        ]
    },
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
}
```


## Create a new Rule

An application can create a Rule by issuing an HTTP POST request to the URL of the containing Test Plan resource

### Request

#### URL
`/testplan/:testplan_id/rule`

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
| ruleType | A string value that specifies `request` or `response`.|

#### Request example

```
POST https://api.heliosburn.com/testplan/1/rule HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "ruleType": "response",
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
Location: http://api.heliosburn.com/rule/1
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5

{
	"id": 1
}
 ```


## Update Rule details

An application can update a Rule by issuing an HTTP PUT request to the URL of the containing Rule resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the Rule. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/testplan/:testplan_id/rule/:rule_id`, for example, `/testplan/9/rule/1` to update the Rule with ID 1 within Test Plan 9.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Rule representation with the elements to be modified:

| Element | Description |
|---|---|
| ruleType | A string value that specifies `request` or `response`.|
| testPlanId | An ID identifying the testplan_id a rule belongs to.|

 #### Request example

```
PUT https://api.heliosburn.com/testplan/9.rule/1 HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
    "ruleType": "request",
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


## Delete a Rule

An application can permanently delete a Rule by issuing an HTTP DELETE request to the URL of the Rule resource. It's a good idea to precede DELETE requests like this with a caution note in your application's user interface.

### Request

#### URL
`/testplan/:testplan_id/rule/:rule_id`, for example, `/testplan/1/rule/19` to delete the Rule with ID 19 within Test Plan 1.

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
DELETE https://api.heliosburn.com/testplan/1/rule/19 HTTP/1.1
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





# Actions

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
`/session/:id/stop`, for example, `/session/23/stop` to start the Session with ID 23.

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

## Get HeliosBurn status

To retrieve information the status of the HeliosBurn proxy server, an application submits an HTTP GET request to the URL that represents the Status resource.

### Request

#### URL
`/status`

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
| status | Status of the proxy server. It can either be `idle` or `busy`. |

If the `status` element is `busy`, the response body will also contain the following elements:

| Element | Description |
|---|---|
| busySince | A dateTime value that specifies the date and time since the proxy server has been busy. |
| busyWith | The URL of the resource that is running in the server, so that the user can stop or get more information about the execution. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The User information is in the response body. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response example

When the server is idle:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Date: Fri, 22 Oct 2014 08:01:54 GMT
Server: Noelios-Restlet-Engine/1.1.5
{
    "status": "idle"
}
```

When the server is busy:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Date: Fri, 22 Oct 2014 08:01:54 GMT
Server: Noelios-Restlet-Engine/1.1.5
{
    "status": "busy",
    "busySince": "2014-02-12 03:34:51",
    "busyWith": "https://api.heliosburn.com/session/23"
}
```



## Get current traffic

To retrieve the current traffic that is being handled by HeliosBurn, an application submits an HTTP GET request to the URL that represents the Traffic resource.

### Request

#### URL
`/traffic`

#### Method
GET

#### Query Parameters

The request accepts the following query parameters:

| Field | Description |
|---|---|
| from | The ID of the last request. |
| max | The maximum number of requests to be returned by HeliosBurn. Any value greater than `x` will be truncated to `x`. |

#### Request example

```
GET https://api.heliosburn.com/traffic?from=42&max=10 HTTP/1.1
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
| Content-Length | The length of the retrieved content. |

#### Response Body

The response body contains the following elements in JSON format:

| Element | Description |
|---|---|
| count | An integer value that represents the number of requests contained in the `request` element. |
| more | A boolean value that indicates whether there are more requests to be pulled at the time of processing the call. |
| requests | A list of Request resource chronologically ordered (from the oldest to the most recent). |

The `request` element contains the following subelements in JSON format:

| Element | Description |
|---|---|
| id | An integer value that represents the ID of the Request resource. |
| createdAt | A dateTime value that specifies the date and time the request was received. |
| httpProtocol | HTTP protocol. |
| method | HTTP method. |
| url | URL. |
| response | A Response resource representation. |

The `response` element contains the following subelements in JSON format:
| Element | Description |
|---|---|
| id | An integer value that represents the ID of the Response resource. |
| createdAt | A dateTime value that specifies the date and time the request was received. |
| httpProtocol | HTTP protocol. |
| statusCode | HTTP Status code. |
| statusCode | HTTP Status description. |

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
{
	"count": 3,
	"more": false,
	"requests": [
		{
			"id": 45,
			"createdAt": "2014-02-12 03:34:51",
			"httpProtocol": "HTTP/1.1",
			"method": "GET",
			"url": "http://api.example.com/resource1",
			"response": {
				"id": 60,
				"createdAt": "2014-02-12 03:34:52",
				"httpProtocol": "HTTP/1.1",
				"statusCode": "200",
				"statusDescription": "OK"
			}
		},
		{
			"id": 46,
			"createdAt": "2014-02-12 03:34:51",
			"httpProtocol": "HTTP/1.1",
			"method": "PUT",
			"url": "http://api.example.com/resource3",
			"response": {
				"id": 61,
				"createdAt": "2014-02-12 03:34:52",
				"httpProtocol": "HTTP/1.1",
				"statusCode": "404",
				"statusDescription": "Not Found"
			}
		},
		{
			"id": 47,
			"createdAt": "2014-02-12 03:34:51",
			"httpProtocol": "HTTP/1.1",
			"method": "POST",
			"url": "http://api.example.com/resource5",
			"response": {
				"id": 62,
				"createdAt": "2014-02-12 03:34:52",
				"httpProtocol": "HTTP/1.1",
				"statusCode": "201",
				"statusDescription": "Created"
			}
		}
	]
}
```
