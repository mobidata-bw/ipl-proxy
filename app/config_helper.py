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

from pathlib import Path
from typing import Any

from yaml import safe_load


class ConfigHelper:
    _config: dict

    def __init__(self):
        config_path = Path(Path(__file__).parents[1], 'config.yaml')

        if config_path.exists():
            with open(config_path) as config_file:
                self._config = safe_load(config_file)
        else:
            self._config = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
