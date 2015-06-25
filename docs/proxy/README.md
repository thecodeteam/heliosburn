## HeliosBurn Proxy Service

* [Overview](#overview)
* [Proxy Service](#the-proxy-service)
* [Recording Traffic](#recording_traffic)
* [Fault Injection Sessions](injection.md)
* [Testing](testing.md)


# Overview

The proxy service is at the heart to of HeliosBurn's fault injection capabilities by implementing man-in-the-middle interception of HTTP traffic.


# The proxy service

The proxy service is responsible for managing and controlling all aspects of fault injection afforded by HeliosBurn.

The service can be started independently with the following command:

`python proxy`

For more details review the following documents:

* [Service](service.md) - Detailed description of the proxy service, including configuration and command line options. (`administrators`)

* [Service API](api.md) - Detailed description of the service API used to interact with the proxy service. (`developers`)

# Recording Traffic

If instructed the proxy service will record traffic for use with HeliosBurn test plans. Recording should be initiated through the HeliosBurn webui, rather than through the proxy directly. For detailed information on how traffic is recorded by the proxy service please see the following document:

* [Recording](recording.md) - Detailed description of how the proxy records traffice (`developers`)

# Fault Injection Sessions

The primary purpose of the proxy service is to inject various types of fault into client/server traffic. The proxy service accomplishes this through a set of pluggable session injection modules that can be started and stopped through the `Service API`.  For details on the individual modules see the following documents:

* [Injection Module](injection.md) - A detailed description of the injection module. This module is responsible for injecting changes to request and response headers given a set of rules.(`administrators` and `developers`)

* [Quality Of Service Module](qos.md) - A detailed description of the quality fo service module. This module simulates a `quality of service` based on a pre-defined QOS profile. (`administrators` and `developers`)

* [Server Overload Module](server_overload.md) - A detailed description of the server overload module. This module simulates server overload scenarios based on a pre-defined server overload profile. (`administrators` and `developers`)

* [Module Development](module_developer.md)  - Guide to developing additional modules for the proxy service. (`developers`)
