"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""


from app.base_converter import BaseConverter


class StadtnaviChargepointConverter(BaseConverter):
    hostnames = ['api.dev.stadtnavi.eu']

    def convert(self, data: dict, path: str, **kwargs) -> dict:
        if path != '/herrenberg/charging-stations/charging-stations-ocpi.json':
            return data

        for location in data.get('data', []):
            for evse in location.get('evses', []):
                evse['status'] = 'AVAILABLE'

        return data
