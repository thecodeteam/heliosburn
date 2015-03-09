- [Rule](#rule)
  - [Get a list of Rules](#get-a-list-of-rules)
  - [Get Rule details](#get-rule-details)
  - [Create a new Rule](#create-a-new-rule)
  - [Update Rule details](#update-rule-details)
  - [Delete a Rule](#delete-a-rule)
- [Examples](#example-rules)

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


## Get a list of Rules

To retrieve a list of Rules, an application submits an HTTP GET request to the URL that represents the Rule resource.

### Request

#### URL
`/rule/`

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

The response body contains a `rules` key containing a list of available rules.

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
`/rule/:rule_id`, for example, `/rule/j34k2b5l3425bl3425l03`.

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

The response body contains a Rule represented in JSON format.

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

An application can create a Rule by issuing an HTTP POST request to the following endpoint.
### Request

#### URL
`/rule`

#### Method
POST

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Rule, as specified in [Rule](#Rule):

#### Request example

```
POST https://api.heliosburn.com/rule HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
  'ruleType': 'request',
  'filter': {
      'httpProtocol': 'HTTP/1.1',
      'method': 'GET',
      'headers': [
          {'key': 'User-Agent'},
          {'key': 'X-Middleman', 'value': 'MS ISA'},
      ],
  },
  'action': {
      'type': 'modify',
      'method': 'PUT',
      'setHeaders': [
          {
              'key': 'User-Agent', 'value': 'lynx',
          },
      ],
      'deleteHeaders': [
          {
              'key': 'X-Middleman',
          },
      ],
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
| Location | The location of the newly created Rule. |

#### Status Codes

| Status Code | Description |
|---|---|
| 200-299 | The request was successful. The Rule was successfully created. |
| 400 | Bad request. Typically returned if required information was not provided as input. |
| 500-599 | Server error. |

#### Response Example

```
HTTP/1.1 201 Created
Content-Type: application/octet-stream; charset=UTF-8
Content-Length: 0
Date: Wed, 14 Dec 2014 19:35:02 GMT
Location: http://api.heliosburn.com/rule/fea393x900a1b
Access-Control-Allow-Origin: *
Server: Noelios-Restlet-Engine/1.1.5

{
	"id": "fea393x900a1b"
}
 ```


## Update Rule details

An application can update a Rule by issuing an HTTP PUT request to the URL of the containing Rule resource.
In addition, the app needs to provide as input, JSON that identifies the new attribute values for the Rule. Upon receiving the PUT request, the HeliosBurn service examines the input and updates any of the attributes that have been modified.

### Request

#### URL
`/rule/:rule_id`, for example, `/rule/foo` to update the Rule with ID 'foo'.

#### Method
PUT

#### Request Header
The request header includes the following information:

| Field | Description |
|---|---|
| Content-Type | The content type and character encoding of the response. |
| Content-Length | The length of the retrieved content. |

#### Request Body

JSON input that contains a Rule representation with the elements to be modified, and must conform to the specifications listed in [Rule](#rule).

 #### Request example

```
PUT https://api.heliosburn.com/rule/foo HTTP/1.1
User-Agent: Jakarta Commons-HttpClient/3.1
Host: api.heliosburn.com
Content-Length: 294
Content-Type: application/json; charset=UTF-8

{
  'ruleType': 'request',
  'filter': {
      'httpProtocol': 'HTTP/1.1',
      'method': 'GET',
      'headers': [
          {'key': 'User-Agent'},
          {'key': 'X-Proxy', 'value': 'Squid'},
      ],
  },
  'action': {
      'type': 'modify',
      'method': 'GET',
      'setHeaders': [
          {
              'key': 'User-Agent', 'value': 'curl',
          },
      ],
      'deleteHeaders': [
          {
              'key': 'X-Proxy',
          },
      ],
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
| 200-299 | The request was successful. The Rule was successfully updated. |
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
`/rule/:rule_id`, for example, `/rule/foo` to delete the Rule with ID 'foo'.

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
DELETE https://api.heliosburn.com/rule/foo HTTP/1.1
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
| 200-299 | The request was successful. The Rule was successfully deleted. |
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

# Example Rules

Rules have a very detailed specification(as seen in [Rule](#rule)). Creating these can be tricky, so the following JSON examples are provided to help guide you in creating your own Rules.

#### Match GET requests from User-Agent 'Firefox'

```
{
  'ruleType': 'request',
  'filter': {
    'method': 'GET',
    'headers': [{'key': 'User-Agent', 'values': '.*Firefox.*'}]
  }
}
```

The above rule matches requests that use the method `GET`, and specifically looks for `User-Agent` header that matches the regular expression `.*Firefox.*`. There is no action associated with this rule. If we wanted to drop traffic that matched this rule, we would include an `action` within the rule. Below is the same filter, with the `action` to drop the request.

#### Drop GET requests from User-Agent 'Firefox'

```
{
  'ruleType': 'request',
  'filter': {
    'method': 'GET',
    'headers': [{'key': 'User-Agent', 'values': '.*Firefox.*'}]
  }
  'action': {
    'type': 'drop'
  }
}
```
