"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
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

    def get(self, key: str, default: Any) -> Any:
        return self._config.get(key, default)
