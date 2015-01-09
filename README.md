HeliosBurn
==========

### Helios Burn - A REST Fault Injection Platform


Helios Burn is a REST fault injection platform that captures HTTP and HTTPS traffic and logs it for users to review. Helios Burn provides the capability to modify HTTP traffic, thus injecting faults, as it is being sent by the client or received from the server. The purpose of Helios Burn is to provide developers with a tool that inject failures and instabilities so that they can verify the stability and resilience of their applications and identify and prevent failures before deploying them into a production environment.


Helios Burn can be deployed in a standalone server, in a Virtual Machine, or co-located with the Web server or Client application.

It implements a man-in-the-middle interception using self-signed certificates to be able to intercept and interpret HTTPS traffic.

![Helios-Burn-Overview](https://github.com/emccode/HeliosBurn/blob/master/docs/figures/Helios-Burn-Overview.png "Helios Burn Overview")

In general terms, the traffic flow is as follows:

    The Helios Burn proxy gets requests from clients that are willing to access resources exposed by a REST application running on a web server (e.g. Amazon S3, OpenStack Swift, EMC Atmos, etc...).

    The proxy processes the request performing modification depending on certain criteria.

    The proxy forwards the processed request to the server on behalf of the client.

    The proxy receives the response from the server.

    The proxy processes the response performing modifications depending on certain criteria.

    The proxy returns the processed response to the client on behalf of the server.



