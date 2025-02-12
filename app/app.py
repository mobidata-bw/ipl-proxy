"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

import json
import logging
from importlib import import_module
from inspect import isclass
from json import JSONDecodeError
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, List

from mitmproxy.http import HTTPFlow

from app.base_converter import BaseConverter
from app.config_helper import ConfigHelper

logger = logging.getLogger('converters.requests')


class App:
    json_converters: Dict[str, List[BaseConverter]]

    def __init__(self):
        self.config_helper = ConfigHelper()

        self.json_converters = {}

        # the following code is a converter autoloader. It dynamically adds all converters in ./converters.
        package_dir = Path(__file__).resolve().parent.joinpath('converters')
        for _, module_name, _ in iter_modules([str(package_dir)]):
            # load all modules in converters
            module = import_module(f'app.converters.{module_name}')
            # look for attributes
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isclass(attribute):
                    if not issubclass(attribute, BaseConverter) or attribute is BaseConverter:
                        continue
                    # at this point we can be sure that attribute is a BaseConverter child, so we can instantiate and use it
                    obj = attribute()
                    for hostname in obj.hostnames:
                        if hostname not in self.json_converters:
                            self.json_converters[hostname] = []
                        self.json_converters[hostname].append(obj)

    def request(self, flow: HTTPFlow):
        if flow.request.host in self.config_helper.get('HTTP_TO_HTTPS_HOSTS', []):
            flow.request.scheme = 'https'
            flow.request.port = 443

    def response(self, flow: HTTPFlow):
        # Log requests
        logger.info(f'GET {flow.request.url}: HTTP {"-" if flow.response is None else flow.response.status_code}')

        # if there is no converter for the requested host, don't do anything
        if flow.request.host not in self.json_converters:
            return

        # try to load the response. If there is any error, return.
        if not flow.response or not flow.response.text:
            return
        try:
            json_data = json.loads(flow.response.text)
        except (JSONDecodeError, TypeError):
            return

        # iterate all converters and apply them
        for json_converter in self.json_converters[flow.request.host]:
            json_data = json_converter.convert(data=json_data, path=flow.request.path)

        # set the returning json content
        flow.response.text = json.dumps(json_data)
