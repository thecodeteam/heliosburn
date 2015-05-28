# HeliosBurn

Helios Burn is a REST fault injection platform that captures HTTP and HTTPS traffic and logs it for users to review.
Helios Burn provides the capability to modify HTTP traffic, thus injecting faults, as it is being sent by the client
or received from the server. The purpose of Helios Burn is to provide developers with a tool that inject failures and
instabilities so that they can verify the stability and resilience of their applications and identify and prevent
failures before deploying them into a production environment.

**Want to try it out? See our [Getting started](docs/getting_started/) guide.**

Helios Burn can be deployed in a standalone server, in a Virtual Machine, or co-located with the Web server or Client
application.

It implements a man-in-the-middle interception using self-signed certificates to be able to intercept and interpret
HTTPS traffic.

![Helios-Burn-Overview](https://github.com/emccode/HeliosBurn/blob/master/docs/figures/Helios-Burn-Overview.png "Helios Burn Overview")





In general terms, the traffic flow is as follows:

1. The Helios Burn proxy gets requests from clients that are willing to access resources exposed by a REST application running on a web server (e.g. Amazon S3, OpenStack Swift, EMC Atmos, etc...).
2. The proxy processes the request performing modification depending on certain criteria.
3. The proxy forwards the processed request to the server on behalf of the client.
4. The proxy receives the response from the server.
5. The proxy processes the response performing modifications depending on certain criteria
6. The proxy returns the processed response to the client on behalf of the server.


## For Developers

The best way to get started with HeliosBurn development is taking a look at the [DEVELOPERS.md](DEVELOPERS.md) file. The document will walk you through setting up a development environment in a Vagrant box and configure PyCharm use it. This environment is ideal because it contains all needed packages and tools required by HeliosBurn.

If you would like to start contributing, check out these [notes](CONTRIBUTING.md) to help you get started.

### Code Organization

- docs/: Documentation
- heliosburn/: HeliosBurn core code
  - django/: Django project that encompasses the WebUI and the API
  - proxy/: Proxy engine
  - fault-injection/: Fault Injection engine and module
  - recorder/: Recorder engine and module
  - db_model: Database model
- puppet/: Puppet configuration and modules


### HeliosBurn API

HeliosBurn API is documented here: 

- [Authentication](https://github.com/emccode/HeliosBurn/blob/master/docs/api/authentication.md "Authentication")
- [User](https://github.com/emccode/HeliosBurn/blob/master/docs/api/user.md "User")
- [Session](https://github.com/emccode/HeliosBurn/blob/master/docs/api/session.md "Session")
- [Test Plan](https://github.com/emccode/HeliosBurn/blob/master/docs/api/testplan.md "Test Plan")
- [Rule](https://github.com/emccode/HeliosBurn/blob/master/docs/api/rule.md "Rule")
- [Recording](https://github.com/emccode/HeliosBurn/blob/master/docs/api/recording.md "Recording")
- [Proxy](https://github.com/emccode/HeliosBurn/blob/master/docs/api/proxy.md "Proxy")

### Data Flow

The core of HeliosBurn is a Twisted reactor that listens for TCP connections. The entry point of the proxy is a Twisted resource called `HeliosBurnResource` located in `heliosburn/proxy/proxy_core.py`. From there, the `HeliosBurnRequest` takes care of all incoming requests by passing them through all enabled modules and eventually establishing a connection with the upstream server and sending them through. Responses are handled by the `HeliosBurnClient` and, again, passed to the modules and back to clients.

##Contributing to HeliosBurn

The Helios Burn project has been licensed under the  [MIT](http://opensource.org/licenses/MIT "The MIT License (MIT)") License. In order to contribute to the HeliosBurn project you will do do two things:


1. License your contribution under the [DCO](http://elinux.org/Developer_Certificate_Of_Origin "Developer Certificate of Origin") + [MIT](http://opensource.org/licenses/MIT "The MIT License (MIT)")
2. Identify the type of contribution in the commit message



### 1. Licensing your Contribution: 

As part of the contribution, in the code comments (or license file) associated with the contribution must include the following:

“The MIT License (MIT)

Copyright (c) [Year], [Company Name (e.g., EMC Corporation)]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  The above copyright notice and this permission notice shall be included in  all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This code is provided under the Developer Certificate of Origin- [Insert Name], [Date (e.g., 1/1/15]”


**For example:**

A contribution from **Joe Developer**, an **independent developer**, submitted in **May 15th of 2015** should have an associated license (as file or/and code comments) like this:
 
“The MIT License (MIT)

Copyright (c) 2015, Joe Developer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  The above copyright notice and this permission notice shall be included in  all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This code is provided under the Developer Certificate of Origin- Joe Developer, May 15th 2015”

### 2. Identifying the Type of Contribution

In addition to identifying an open source license in the documentation, **all Git Commit messages** associated with a contribution must identify the type of contribution (i.e., Bug Fix, Patch, Script, Enhancement, Tool Creation, or Other).


## Licensing

HeliosBurn is licensed under the  [MIT](http://opensource.org/licenses/MIT "The MIT License (MIT)") license: 

“The MIT License (MIT)

Copyright (c) 2015, EMC Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Support

Please file bugs and issues at the Github issues page. For more general discussions you can contact the EMC Code team at <a href="https://groups.google.com/forum/#!forum/emccode-users">Google Groups</a> or tagged with **EMC** on <a href="https://stackoverflow.com">Stackoverflow.com</a>. The code and documentation are released with no warranties or SLAs and are intended to be supported through a community driven process.
