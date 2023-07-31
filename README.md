# MobiData BW Modification Proxy

This small project is able to convert data on the fly. This is sometimes necessary to fix invalid data.

## How to install

### Virtual Environment

You can use following commands to create a virtual environment and install all necessary packages:

```shell
# create the virtual environment
virtualenv venv
# go into the virtual environment
source venv/bin/activate
# install all required packages
pip install -r requirements.txt
```

## How to use

With virtual environments, you can start `mitmproxy` with our converters like this:

```shell
mitmdump -s addons.py
```

You can also use the interactive mode by

```shell
mitmproxy -s addons.py
```

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
