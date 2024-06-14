"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from app.base_converter import BaseConverter
from app.utils.gbfs_util import update_stations_availability_status


class GbfsNextbikeVehicleAvailabilityConverter(BaseConverter):
    """
    Nextbike's station_status feeds currently don't provide the vehicle_types_available property.
    But their vehicles at stations have a station_id assigned.

    This Converter counts the number of vehicles per vehicle_type_id at each station and
    constructs the vehicle_types_available from this information.

    In cases not a single vehicle is assigned to a station, we add
    a single vehicle_types_id with count == 0 as vehicle_types_available.

    Note that this is a workaround and might be a vehicle_type that will never be
    available at this station, or a vehicle_type which could be available sometimes
    will not appear in vehicle_types_available.
    """

    hostnames = ['gbfs.nextbike.net']

    free_vehicles_cache_per_system: dict[str, list[dict]] = {}

    def convert(self, data: dict | list, path: str) -> dict | list:
        if (
            not isinstance(data, dict)
            or not path.startswith('/maps/gbfs/v2/')
            or not (path.endswith('/station_status.json') or path.endswith('/free_bike_status.json'))
        ):
            return data

        system_id = self._get_system_id_from_path(path)

        if path.endswith('/free_bike_status.json'):
            return self._convert_free_vehicle_status(system_id, data, path)

        return self._convert_station_status(system_id, data, path)

    @staticmethod
    def _get_system_id_from_path(path: str) -> str:
        return path.split('/')[-3:-2][0]

    def _convert_free_vehicle_status(self, system_id: str, data: dict, path: str) -> dict:
        # cache vehicles per feed
        vehicles = data.get('data', {}).get('bikes', [])
        if isinstance(vehicles, list):
            self.free_vehicles_cache_per_system[system_id] = vehicles
        return data

    def _convert_station_status(self, system_id: str, data: dict, path: str) -> dict:
        if not data.get('data', {}).get('stations'):
            return data

        vehicles = self.free_vehicles_cache_per_system.get(system_id, [])

        update_stations_availability_status(data['data']['stations'], vehicles)

        return data
