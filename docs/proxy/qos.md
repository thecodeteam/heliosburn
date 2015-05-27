- [Quality of Service Module](#quality-of-service-odule)
  - [QoS Profile](#qos-profile)
  - [Latency](#latency)
  - [Jitter](#jitter)
  - [Packet Loss](#packet-loss)

# Quality of Service Module

  ![alt text](../figures/QOS_Module.png "Altering QoS")



# QOS Module

The QOS module is situated inside the proxy processing pipline so as to apply a given QoS profile to proxy traffic. When the QoS module is started the given `profile_id` is used to retrieve the QoS profile from `mongo`. When the module receives a response or request, each QoS action is applied to the traffic as defined by the retrieved QoS profile.

## QoS Profile

 The profile will then be used by the QoS module to determine the specific quality of service applied to proxy traffic.

The following possible actions are implemented as command objects and executed with the parameters given by the QoS_profile:

| Action      | Context | Description |
|:------------|:--------|:------------|
| Latency     | request | Injectes a constant wait time into the the traffic stream so as to increase the round-trip time of each request |
| Jitter      | request | Injects random wait time into the traffic stream so as to increase the round-trip time of each request inconsistently |
| Packet Loss | both    | Drops requests/responses randomly |
|

## Latency

An action type of `latency` has the following parameters.

| Element           | Context  | Description |
|:------------------|:---------|:-----------------------------------------------|
| maximum           | request  | The maximum amount of time, in seconds, the module will inject. |
| minimum           | request  | The minimum amount of time, in seconds, the module will inject. |

## Jitter

An action type of `Jitter` has the following parameters.

| Element           | Context  | Description |
|:------------------|:---------|:-----------------------------------------------|
| maximum           | request  | The maximum amount of time, in seconds, the module will inject. |
| minimum           | request  | The minimum amount of time, in seconds, the module will inject. |

## Packet Loss

An action type of `Packet Loss` has the following parameters.

| Element           | Context  | Description |
|:------------------|:---------|:-----------------------------------------------|
| chance            | both     | The percentage chance that any given request/response will be lost. |

