"""
MobiData BW Proxy
Copyright (c) 2025, binary butterfly GmbH

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

import functools
import json
import logging
import secrets
import string
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from app.utils.default_json_encoder import DefaultJSONEncoder


class BaseAttributeFormatter(logging.Formatter, ABC):
    label_allowed_chars: str = f'{string.ascii_letters}{string.digits}_.'
    service_name: str
    prefix: str

    def __init__(self, *args, prefix: str, service_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(self.build_payload(record), cls=DefaultJSONEncoder)

    def add_additional_attributes(self, record_attributes: dict[str, Any]):
        pass

    @staticmethod
    def get_trace_id() -> str:
        return secrets.token_hex(16)

    @staticmethod
    def get_span_id() -> str:
        return secrets.token_hex(8)

    @functools.lru_cache(256)  # noqa: B019
    def format_label(self, label: str | Enum) -> str | None:
        if isinstance(label, Enum):
            label = label.name

        # The label uses way fewer characters then allowed, just a-z0-9_
        cleaned_label = ''.join(char for char in label if char in self.label_allowed_chars)
        if len(cleaned_label) == 0:
            return None
        return f'{self.prefix}.{cleaned_label.lower()}'

    def build_attributes(self, record: logging.LogRecord) -> dict[str, Any]:
        record_attributes: dict[str, Any] = {}

        self.add_additional_attributes(record_attributes)

        if hasattr(record, 'attributes'):
            record_attributes.update(getattr(record, 'attributes'))

        attributes = {}

        for attribute_name, attribute_value in record_attributes.items():
            cleared_name = self.format_label(attribute_name)
            if cleared_name is not None:
                attributes[cleared_name] = attribute_value

        return attributes

    @abstractmethod
    def build_payload(self, record: logging.LogRecord) -> dict[str, Any]: ...
