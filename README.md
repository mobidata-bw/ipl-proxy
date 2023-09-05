# MobiData BW Modification Proxy

**An HTTP proxy that transforms request and response bodies on the fly.**

This proxy service fixes invalid data, or abstracts away other data access hurdles (e.g. bespoke authentication schemes), **so that other services in the MobiData-BW *Integrationsplatform* (IPL) can consume the datasets as-is**.

## How to install

*Note:* This project to is designed to be run as a part of the entire IPL platform, [as defined in the `ipl-orchestration` repo](https://github.com/mobidata-bw/ipl-orchestration). But you can also run it in a standalone fashion.

### Virtual Environment

You can use following commands to create a virtual environment and install all necessary packages:

```shell
# create the virtual environment
virtualenv venv
# go into the virtual environment
source venv/bin/activate
# install all required packages
pip install -r requirements.txt -r requirements-dev.txt
```

### Docker

You can use Docker to start the MobiData BW Modification Proxy, too. There is a `Makefile` which helps with default
commands. Setting everything up and starting the container in foreground is the default target, so for a start just 
use the command `make`.

The docker container should not run as root. In order to have a proper user mapping, docker compose expects UID and GID
by env variable. The Makefile automatically sets this by putting the environment in your local `.env` file.


## How to use

With virtual environments, you can start `mitmproxy` with our converters like this:

```shell
mitmdump -s addons.py
```

You can also use the interactive mode by

```shell
mitmproxy -s addons.py
```

If you want to have access to a config, you have to create a config.yaml. You can use the template in 
`config_dist_dev.yaml`:

```shell
cp config_dist_dev.yaml config.yaml
```

Using docker, you just have to use `make` to start the `mitmdump` service. The `config.yaml` is created with default
values automatically.

The HTTP proxy will be available at `http://localhost:8080`.


## Caveats

### TLS

Mitmproxy automatically creates an own certificate authority and stores them at `~/.mitmproxy`. The response is encrypted 
with this new self-signed CA. The client should not know about this CA, so it will run into TLS errors. It can be
solved in two ways:

1) Ignore the TLS cert completely.
2) Make the self-signed CA available at your client.

For curl, this means following parameters:

```shell
# first way
curl -x "http://localhost:8080" https://your-target.tld/data -k
# second way
curl -x "http://localhost:8080" https://your-target.tld/data --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem
```

At docker, `~` is set to the folder where this Readme is placed, so you have to modify the path to point to this 
location. 
