# Getting started with Helios Burn

To deploy Helios Burn, you have several options: [Docker](https://www.docker.com), [Vagrant](https://www.vagrantup.com/), or a virtual machine on a platform of your choice. This guide will focus on Vagrant. The purpose of this guide is to get you up and running as quickly as possible, and does not cover all the of the options for deployment and configuration. Please refer to the [Helios Burn documentation](../) to learn more.

## Steps of this guide

1. [Getting Vagrant](#getting-vagrant)
*  [Getting Helios Burn](#getting-helios-burn)
*  [Setting up Helios Burn](#setting-up-your-helios-burn-system-with-vagrant)
*  [Using Helios Burn](#using-helios-burn)

### Getting Vagrant

1. [Download and install Virtualbox](https://www.virtualbox.org/wiki/Downloads)
*  [Download and install Vagrant](http://www.vagrantup.com/downloads.html)

### Getting Helios Burn

You can download Helios Burn from Github using [Git](https://github.com/emccode/HeliosBurn/archive/master.zip) or a direct [HTTP download](https://github.com/emccode/HeliosBurn/archive/master.zip). To clone Helios Burn with `git`, type the following in a terminal:

```
git clone git@github.com:emccode/HeliosBurn.git --recursive
```
__WARNING__: Make sure you include the `--recursive` option above! Otherwise Vagrant will fail to provision our environment.

### Setting up your Helios Burn system with Vagrant

After cloning Helios Burn, enter the directory by typing the following in a terminal:

```
cd HeliosBurn
```

Now launch the Vagrant environment by typing the following in your terminal:

```
vagrant up
```
__NOTE__: Depending on the speed of your computer, this step may take several minutes. This will download, build, and setup the guest operating system to contain Helios Burn.

After your Vagrant is complete, run the following commands in your terminal to install Helios Burn within your Vagrant.

```
vagrant ssh
cd HeliosBurn
sudo ./install_in_vagrant.sh
```
*NOTE: This step is only done once. After Helios Burn is installed, it will start automatically when you type `vagrant up`.*

Helios Burn is now started and ready to use.

### Using Helios Burn

1. [Logging in](#logging-in)
*  [The session manager](#the-session-manager)
*  [Creating a new session](#creating-a-new-session)

##### Logging in
The first thing to do is to log in. Once you have logged in, you will receive a header called `X-Auth-Token`. Using this token associates requests with your user. Tokens expire (by default) after 1 hour of inactivity. To obtain your token, run the following from a terminal on your host.

    curl -v -XPOST 'http://localhost:8100/api/auth/login' -d \
        '{"username":"admin", "password":"admin"}'

The output should resemble the following, but your `X-Auth-Token` will be unique. You should copy your token for future use in this guide. This guide will use the token presented below, but remember to replace it with your unique token, or you will receive `HTTP 401 UNAUTHORIZED` for your requests.

    smallpaw:~ hgrubbs$ curl -v -XPOST 'http://localhost:8100/api/auth/login' -d \
    >     '{"username":"admin", "password":"admin"}'
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8100 (#0)
    > POST /api/auth/login HTTP/1.1
    > Host: localhost:8100
    > User-Agent: curl/7.42.1
    > Accept: */*
    > Content-Length: 40
    > Content-Type: application/x-www-form-urlencoded
    > 
    * upload completely sent off: 40 out of 40 bytes
    < HTTP/1.1 200 OK
    < Vary: Cookie
    < X-Frame-Options: SAMEORIGIN
    < Content-Type: text/html; charset=utf-8
    < X-Auth-Token: 910480523f565b1fbfbf67cfaf7445763aad744834caf4cf8c75715ad476b402e57fed4f6ea350d4fc72502aa550393aa4430d0908a75e0f7efb2772dca8dfe9
    < Transfer-Encoding: chunked
    < Date: Wed, 20 May 2015 18:58:22 GMT
    < Server: heliosburn-vm
    < 
    * Connection #0 to host localhost left intact


##### Create a new session

Now let's create a session. A session will serve to associate our HTTP traffic, testplan, and rules together. Run the following in a terminal your host, and remember to replace the `X-Auth-Token` with your own.

    curl -XPOST 'http://localhost:8100/api/session/' -d \
        '{
           "name": "test session #1", 
           "description": "my first helios burn session",
           "upstreamHost": "localhost",
           "upstreamPort": 8080 
          }' \
        -H 'X-Auth-Token: 910480523f565b1fbfbf67cfaf7445763aad744834caf4cf8c75715ad476b402e57fed4f6ea350d4fc72502aa550393aa4430d0908a75e0f7efb2772dca8dfe9'

The output will be a JSON, containing a unique session id. Copy this id, so you can use it during this guide.

##### Create a new testplan

Now let's create a testplan. A testplan contains the rules and actions that the proxy will attempt to apply to HTTP traffic. Let's include a simple rule in our testplan, that changes HTTP GET requests into HTTP POST, if a certain header is present. Run the following in a terminal on your host, and remember to replace the `X-Auth-Token` with your own.

    curl -XPOST 'http://localhost:8100/api/testplan/' -g -d \
        '
                {
                  "name": "my first testplan",
                  "rules": [
                    {
                      "name": "GET to POST",
                      "ruleType": "request",
                      "filter": {
                        "method": "GET"
                      },
                      "action": {
                        "type": "modify",
                        "method": "POST"
                      }
                    }
                  ]
                }' \
        -H 'X-Auth-Token: 38ed1a7265be4ddf7f7f038c19eaa908ea2c0f4d511830760c86cb759df71993844f6288a60469ff838a024992da3cd205b407bb7c4f47b4e4a27c765e299a2b'

The output will be a JSON, containing a unique testplan id. Copy this id, so you can use it during this guide.

#### Associate your testplan with your session

Now we need to link the session and the testplan you created to each other. Run the following in your host, and remember to replace the token, session id, and testplan id with your own.

    curl -XPUT 'http://localhost:8100/api/session/555ce14ceb908907d690a2ad/' \
        -d '
            {
              "testplan": "555ce114eb908907d690a2ac"
            }' \
        -H 'X-Auth-Token: 38ed1a7265be4ddf7f7f038c19eaa908ea2c0f4d511830760c86cb759df71993844f6288a60469ff838a024992da3cd205b407bb7c4f47b4e4a27c765e299a2b' 

This command should not produce any output if successful. For more details, you could add the `-v` parameter to curl, which would show the resulting status code(`HTTP 200 OK`).


#### Start your session

Now we need to instruct the proxy to begin your session. This causes your testplan and rules to become effective, and Helios Burn will keep track of the traffic they generate. Run the following command in a terminal on your host, and remember to replace the token and session id with your own.

    curl -XPOST 'http://localhost:8100/api/session/555ce14ceb908907d690a2ad/' \
        -H 'X-Auth-Token: 38ed1a7265be4ddf7f7f038c19eaa908ea2c0f4d511830760c86cb759df71993844f6288a60469ff838a024992da3cd205b407bb7c4f47b4e4a27c765e299a2b' 

This command should not produce any output if successful. For more details, you could add the `-v` parameter to curl, which would show the resulting status code(`HTTP 200 OK`).

#### Send traffic to Helios Burn

Let's send some traffic in, and watch our rule take effect. 

    curl -v -XGET 'http://localhost:9000/method_test/' 

Your original request was a GET, however, the server seems to think you sent it a POST. That's due to the rule we created previously, causing the method to be modified.
