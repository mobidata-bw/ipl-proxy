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

import logging

from .base_attribute_formatter import BaseAttributeFormatter


class OpenTelemetryFormatter(BaseAttributeFormatter):
    log_level_mapping: dict[int, int] = {
        logging.DEBUG: 5,
        logging.INFO: 10,
        logging.WARNING: 15,
        logging.ERROR: 20,
        logging.CRITICAL: 25,
    }

    def build_payload(self, record: logging.LogRecord) -> dict:
        return {
            'Timestamp': int(record.created * 1e9),
            'Attributes': {
                **self.build_attributes(record),
                'logger.file_name': record.filename,
                'logger.module_path': record.name,
                'logger.module': record.module,
            },
            'Resource': {
                'service.name': self.service_name,
                'service.pid': record.process,
            },
            'TraceId': self.get_trace_id(),
            'SpanId': self.get_span_id(),
            'SeverityText': 'WARN' if record.levelno == logging.WARNING else record.levelname,
            'SeverityNumber': self.log_level_mapping[record.levelno],
            'Body': record.msg,
        }
