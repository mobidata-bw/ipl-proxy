"""
MobiData BW Proxy
Copyright (c) 2023, systect Holger Bruch
All rights reserved.
"""

import logging
from datetime import datetime
from typing import Any

from app.base_converter import BaseConverter

logger = logging.getLogger('converters.DonkeyFreeBikeStatusConverter')


class DonkeyFreeBikeStatusConverter(BaseConverter):
    """
    Donkey feeds are currently corrupted: free_bike_status.json
    has various issues:

    * properties lat, lon, current_fuel_percent are encoded as strings, not floats
    * vehicle_type_id is missing
    * instead of station_id the property hub_id is returned
    * last_reported is encoded as iso formatted string, while in GBFS v2.3 still seconds since epoch is expected
    """

    hostnames = ['stables.donkey.bike']

    @staticmethod
    def _convert_str_to_float(bike: dict[str, Any], property: str) -> None:
        value = bike.get(property)
        if isinstance(value, str):
            bike[property] = float(value)

    def convert(self, data: dict | list, path: str) -> dict | list:
        if not isinstance(data, dict) or not path.endswith('/free_bike_status.json'):
            return data

        for bike in data['data'].get('bikes', []):
            last_reported = bike.get('last_reported')
            if isinstance(last_reported, str):
                try:
                    bike['last_reported'] = int(datetime.fromisoformat(last_reported).timestamp())
                except Exception:
                    logger.error(f'Failed to parse donkey free_bike_status bike last_reported {last_reported}')
            self._convert_str_to_float(bike, 'lon')
            self._convert_str_to_float(bike, 'lat')
            self._convert_str_to_float(bike, 'current_fuel_percent')
            if 'hub_id' in bike:
                bike['station_id'] = bike.pop('hub_id')
            if 'vehicle_type_id' not in bike:
                if 'current_fuel_percent' in bike:
                    bike['vehicle_type_id'] = 'ebike'
                else:
                    bike['vehicle_type_id'] = 'bicycle'
        return data
