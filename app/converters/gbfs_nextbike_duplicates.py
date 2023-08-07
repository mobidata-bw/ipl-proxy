"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import List, Union

from app.base_converter import BaseConverter


class GbfsNextbikeDuplicatesConverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict) or not path.startswith('/maps/gbfs/v2/') or not path.endswith('/vehicle_types.json'):
            return data

        if not data.get('data', {}).get('vehicle_types'):
            return data

        known_ids: List[str] = []
        filtered_vehicle_types: List[dict] = []

        for vehicle_type in data['data']['vehicle_types']:
            if vehicle_type.get('vehicle_type_id') in known_ids:
                continue
            known_ids.append(vehicle_type.get('vehicle_type_id'))
            filtered_vehicle_types.append(vehicle_type)

        data['data']['vehicle_types'] = filtered_vehicle_types
        return data
