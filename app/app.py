"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH

Licensed under the EUPL, Version 1.2 or – as soon they will be approved by
the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

https://joinup.ec.europa.eu/software/page/eupl

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and
limitations under the Licence.
"""

import json
import logging
import traceback
from importlib import import_module
from inspect import isclass
from json import JSONDecodeError
from logging.config import dictConfig
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, List

from mitmproxy.http import HTTPFlow, Response

from app.base_converter import BaseConverter
from app.config_helper import ConfigHelper
from app.utils import ContextHelper
from app.utils.context_helper import context_helper
from app.utils.default_json_encoder import DefaultJSONEncoder

logger = logging.getLogger(__name__)


class App:
    config_helper: ConfigHelper
    context_helper: ContextHelper

    json_converters: Dict[str, List[BaseConverter]]

    def __init__(self):
        self.config_helper = ConfigHelper()
        self.context_helper = context_helper

        # configure logging
        dictConfig(self.config_helper.get('LOGGING'))

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
        self.context_helper.initialize_context()

        if flow.request.host in self.config_helper.get('HTTP_TO_HTTPS_HOSTS', []):
            flow.request.scheme = 'https'
            flow.request.port = 443

        self.context_helper.set_attribute('url.host', flow.request.host)
        self.context_helper.set_attribute('url.scheme', flow.request.scheme)
        self.context_helper.set_attribute('url.port', flow.request.port)
        self.context_helper.set_attribute('url.path', flow.request.path)

    def response(self, flow: HTTPFlow):
        # Log requests
        logger.debug(f'{flow.request.method} {flow.request.url}: HTTP {"-" if flow.response is None else flow.response.status_code}')

        # if there is no converter for the requested host, don't do anything
        if flow.request.host not in self.json_converters:
            logger.warning('No JSON converter for request.')
            return

        # try to load the response. If there is any error, return.
        if not flow.response:
            logger.warning('No response for request.')
            return

        response: Response = flow.response

        if not response.text:
            logger.warning('Empty response for request.')
            return

        try:
            json_data = json.loads(response.text)
        except (JSONDecodeError, TypeError):
            logger.warning(f'Invalid JSON in request: {response.text}.')
            return

        # iterate all converters and apply them
        for json_converter in self.json_converters[flow.request.host]:
            self.context_helper.set_attribute('converter', json_converter.__class__.__name__)
            try:
                json_data = json_converter.convert(data=json_data, path=flow.request.path)
            except Exception as e:
                logger.error(
                    f'Converter {json_converter.__class__.__name__} threw an exception {e.__class__.__name__}: {e}',
                    extra={
                        'attributes': {
                            # This needs to be json_data, as json_data is maybe already transformed
                            'data': json.dumps(json_data),
                            'traceback': traceback.format_exc(),
                        },
                    },
                )
                return

        # set the returning json content
        flow.response.text = json.dumps(json_data, cls=DefaultJSONEncoder)
