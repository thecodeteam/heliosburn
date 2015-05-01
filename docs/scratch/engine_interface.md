# Engine mockup for fault injection

Explaining arguments to `process_request(http_metadata, session)`

## http_metadata

`http_metadata` Request example:
```json
  "request": {
    "url", "http://foo.com",
    "httpProtocol": "HTTP/1.1",
    "method": "POST",
    "headers": [
      ("Content-Length", "way too long"),
      ("....", "....")
    ]
  }
```

`http_metadata` Response example:
```json
  "request": {
    "url", "http://foo.com",
    "httpProtocol": "HTTP/1.1",
    "method": "POST",
    "headers": [
      ("Content-Length", "way too long"),
      ("....", "....")
    ]
  },
  "response": {
    "httpProtocol": "HTTP/1.1",
    "statusCode": 200,
    "statusDescription": "OK",
    "headers": [
      ("Content-Length", "way too long"),
      ("....", "....")
    ]
  }
```

## session

`session` example:

```json
  "id": 123,
```

# Return values to process_request(...)

## If a rule matches

Returns the `action` component of a `rule` in database.

## If a rule does not match

Returns `None`.
