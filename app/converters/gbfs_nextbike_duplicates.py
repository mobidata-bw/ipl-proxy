"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import List, Union

from app.base_converter import BaseConverter
from app.utils.gbfs import filter_duplicate_vehicle_types

class GbfsNextbikeDuplicatesConverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict) or not path.startswith('/maps/gbfs/v2/') or not path.endswith('/vehicle_types.json'):
            return data

        return filter_duplicate_vehicle_types(data)
