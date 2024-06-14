"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import Union

from app.base_converter import BaseConverter

SECONDS_PER_DAY = 24 * 60 * 60
FOUR_MINUTES = 4 * 60


class DbConnectGbfsTTLConverter(BaseConverter):
    """
    Sets ttl to 240 (= 4 minutes) for free_bike_status and station_status, and to 86400 (=24h) for all other db connect feeds.

    This is necessary DBConnect API imposes rather restrictive rate limits, but does not provide matching ttl information.
    """

    hostnames = ['apis.deutschebahn.com']

    DEFAULT_TTL = SECONDS_PER_DAY

    TTL = {
        'station_status': FOUR_MINUTES,
        'free_bike_status': FOUR_MINUTES,
    }

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict) or not path.startswith('/db-api-marketplace/apis/shared-mobility-gbfs'):
            return data

        endpoint = path[path.rfind('/') + 1 :]

        if 'ttl' in data:
            ttl = self.TTL.get(endpoint, self.DEFAULT_TTL)
            data['ttl'] = ttl

        return data
