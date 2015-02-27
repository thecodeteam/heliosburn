- [Authentication](#authentication)
  - [Login](#login)


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
