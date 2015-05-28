- [Server Overload Module](#server-overload-module)
  - [exponential overload](#exponential-overload)
  - [DoS](#DoS)
  - [servoer overload Profile](#server-overload-profile)

# Server Overload Module

  ![alt text](../figures/HB_Server_Overload_Module.png "Altering QoS")



# Server Overload Module

The server overload module is situated inside the proxy processing pipline so as to apply a given server overload profile to proxy traffic.
When the server overload module is started, the given `session_id` is used to retrieve the server overload profile from `mongo`.
The server overload module actions are then applied to the traffic as defined by the retrieved server overload profile.

## Server Overload Profile

 The server overload profile is used used by the server overload module to determine the specific type and intensity of overload to be applied.
The server overload profile is retrieved from information contained within the session document, specficlially the `serverOverload.id`


### Example session document
```json
{
  "id": 1,
  "name": "Session A",
  "description": "This is a description for a Session",
  "upstreamHost": "github.com",
  "upstreamPort": 80,
  "createdAt": "2014-02-12 03:34:51",
  "updatedAt": "2014-02-12 03:34:51",
  "testPlan":
  {
    "id": 12,
    "name": "ViPR Test plan"
  },
  "qos":
  {
    "id": 45
  },
  "serverOverload":
  {
    "id": 951
  },
  "user":
  {
    "id": 1,
    "username": "John Doe"
  },
  "executions": 42,
}
```

The `serverOverload.id` is then used to make a secod query to retrieve the server overload profile.

### Example server overload profile

```json
{

}
```

The following possible actions are implemented as command objects and executed with the parameters given by the server overload profile:

| Action     | Context | Description                                             |
|:-----------|:--------|:--------------------------------------------------------|
| exponetial | request | An exponential increase in server load                  |
| DoS        | request | An increse in server load comensurate with a DoS attack |
|            |         |                                                         |

## Exponential

An action type of `exponential` has the following parameters.

| Element          | Context | Description                                  |
|:-----------------|:--------|:---------------------------------------------|
| exponent         | request | The exponent used in the increase in load.   |
| initial_requests | request | The initial number of requests to grow from. |

## DoS

An action type of `DoS` has the following parameters.

| Element          | Context | Description                                  |
|:-----------------|:--------|:---------------------------------------------|
| initial_requests | request | The initial number of requests to grow from. |
