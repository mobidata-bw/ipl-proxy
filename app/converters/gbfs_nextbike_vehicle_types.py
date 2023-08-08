"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import List, Union, cast

from app.base_converter import BaseConverter
from app.utils.gbfs import add_missing_max_range_meters, filter_duplicate_vehicle_types


class GbfsNextbikeVehicleTypesCoverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict) or not path.startswith('/maps/gbfs/v2/') or not path.endswith('/vehicle_types.json'):
            return data
        # TODO nextike should provide this information on it's on. 50000 is taken from
        # https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_df/de/free_bike_status.json's
        # "vehicle_type_id":"181","current_fuel_percent":58,"current_range_meters":29000
        default_max_range_meters = 50000
        return add_missing_max_range_meters(filter_duplicate_vehicle_types(cast(dict, data)), default_max_range_meters)
