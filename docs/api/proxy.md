- [Proxy](#proxy)
  - [Get the proxy status](#get-the-proxy-status)
  - [Get current traffic](#get-current-traffic)
  - [Start the proxy](#start-heliosburn-proxy)
  - [Stop the proxy](#stop-heliosburn-proxy)


# Proxy


## Get HeliosBurn status

To retrieve information the status of the HeliosBurn proxy server, an application submits an HTTP GET request to the URL that represents the Status resource.

### Request

#### URL
`/proxy/status`

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

## Start HeliosBurn proxy

To start the proxy server, an application submits an HTTP GET request to the URL that represents the Proxy Start resource.

### Request

#### URL
`/proxy/start?session_id=<session_id>`

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

The response body contains the Proxy response, as detailed in `docs/proxy/api.md`. The API returns this message as a JSON, with the original response within the key `proxyResponse`.

## Stop HeliosBurn proxy

To stop the proxy server, an application submits an HTTP GET request to the URL that represents the Proxy Stop resource.

### Request

#### URL
`/proxy/stop`

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

The response body contains the Proxy response, as detailed in `docs/proxy/api.md`. The API returns this message as a JSON, with the original response within the key `proxyResponse`.
