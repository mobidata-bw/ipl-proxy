"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import Union

from app.base_converter import BaseConverter


class StadtnaviChargepointConverter(BaseConverter):
    hostnames = ['api.dev.stadtnavi.eu']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict) or path != '/herrenberg/charging-stations/charging-stations-ocpi.json':
            return data

        for location in data.get('data', []):
            for evse in location.get('evses', []):
                evse['status'] = 'AVAILABLE'

        return data
