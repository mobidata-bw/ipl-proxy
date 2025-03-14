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

import secrets
from dataclasses import dataclass, field


@dataclass
class Context:
    trace_id: str
    span_id: str
    attributes: dict[str, str | int | float] = field(default_factory=dict)


class InitializationRequiredException(Exception): ...


class ContextHelper:
    _current_context: Context | None

    def initialize_context(self, trace_id: str | None = None, span_id: str | None = None):
        if trace_id is None:
            trace_id = secrets.token_hex(16)
        if span_id is None:
            span_id = secrets.token_hex(8)
        self._current_context = Context(trace_id=trace_id, span_id=span_id)

    def set_attribute(self, key: str, value: str | int | float):
        if self._current_context is None:
            raise InitializationRequiredException()

        self._current_context.attributes[key] = value

    def get_current_attributes(self) -> dict[str, str | int | float]:
        if self._current_context is None:
            raise InitializationRequiredException()

        return self._current_context.attributes

    def get_current_trace_id(self) -> str:
        if self._current_context is None:
            raise InitializationRequiredException()

        return self._current_context.trace_id

    def get_current_span_id(self) -> str:
        if self._current_context is None:
            raise InitializationRequiredException()

        return self._current_context.span_id


# The ContextHelper is initialized globally for logging system access
context_helper = ContextHelper()
