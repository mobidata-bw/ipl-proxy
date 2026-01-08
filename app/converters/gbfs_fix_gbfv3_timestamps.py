import logging
from datetime import UTC, datetime
from typing import Union

from app.base_converter import BaseConverter

logger = logging.getLogger(__name__)


class GbfsFixGbfsV3Timestamps(BaseConverter):
    hostnames = [
        'yoio.rideatom.com',
    ]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        def clean_timestamp(isotimestring: str) -> str:
            try:
                parsed_date = datetime.fromisoformat(isotimestring).replace(microsecond=0)

                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=UTC)

                return parsed_date.isoformat()
            except ValueError:
                logger.error('Could not parse %s as date for %s', isotimestring, path)
                return isotimestring

        if not isinstance(data, dict):
            return data

        if 'last_updated' not in data or not isinstance(data['last_updated'], str):
            return data

        data['last_updated'] = clean_timestamp(data['last_updated'])

        return data
