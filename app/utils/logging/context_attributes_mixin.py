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

from typing import Any

from app.utils.context_helper import context_helper


class ContextAttributesMixin:
    @staticmethod
    def add_additional_attributes(record_attributes: dict[str, Any]):
        record_attributes.update(context_helper.get_current_attributes())

    @staticmethod
    def get_trace_id() -> str:
        return context_helper.get_current_trace_id()

    @staticmethod
    def get_span_id() -> str:
        return context_helper.get_current_span_id()
