"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from app.base_converter import BaseConverter
from app.utils.gbfs_util import set_vehicle_types_available_defaults, update_stations_availability_status


class GbfsNextbikeVehicleAvailabilityConverter(BaseConverter):
    """
    Nextbike's station_status feeds currently don't provide the vehicle_types_available property.
    But their vehicles at stations have a station_id assigned and for some feeds, the
    station names communicate, which form factors might be available at these stations..

    This Converter counts the number of vehicles per vehicle_type_id at each station and
    constructs the vehicle_types_available from this information.

    In cases not a single vehicle is assigned to a station, we add
    * all vehicle types matching the station's form_factor(s) with count == 0 as vehicle_types_available
      (in case these can be deduced from the station name), or
    * a single, random vehicle_types_id with count == 0 as vehicle_types_available.

    Note that the later is a workaround and might be a vehicle_type that will never be
    available at this station, or a vehicle_type which could be available sometimes
    will not appear in vehicle_types_available.
    """

    hostnames = ['gbfs.nextbike.net']

    # For some feeds, the station names include a substring which
    # identifies the form_factors which might be at rent at that station.
    # This mapping defines these mappings.
    STATION_NAME_VEHICLE_TYPE_MAPPINGS_PER_SYSTEM = {
        'nextbike_kk': {
            'RAD Station': ['bicycle'],
            'PLUS Station': ['bicycle', 'cargo_bicycle'],
            'HEIMAT Station': ['cargo_bicycle'],
        }
    }

    free_vehicles_cache_per_system: dict[str, list[dict]] = {}
    form_factors_available_at_station_id: dict[str, dict[str, list[str]]] = {}
    form_factors_by_vehicle_type_id: dict[str, dict[str, str]] = {}

    def convert(self, data: dict | list, path: str) -> dict | list:
        if not isinstance(data, dict) or not path.startswith('/maps/gbfs/v2/'):
            return data

        system_id = self._get_system_id_from_path(path)
        if path.endswith('/station_status.json'):
            return self._convert_station_status(system_id, data, path)

        if path.endswith('/free_bike_status.json'):
            self._cache_free_vehicle_status(system_id, data, path)
        if path.endswith('/station_information.json'):
            self._cache_form_factors_available_at_station_id(system_id, data, path)
        if path.endswith('/vehicle_types.json'):
            self._cache_form_factors_by_vehicle_type_id(system_id, data, path)

        return data

    @staticmethod
    def _get_system_id_from_path(path: str) -> str:
        return path.split('/')[-3:-2][0]

    def _deduce_form_factors_from_station(self, system_id: str, station: dict) -> list[str]:
        # Deduces form factors potentially available at station from it's name.

        if system_id not in self.STATION_NAME_VEHICLE_TYPE_MAPPINGS_PER_SYSTEM:
            return []

        station_name = str(station.get('name'))
        for name_fragment, form_factors in self.STATION_NAME_VEHICLE_TYPE_MAPPINGS_PER_SYSTEM[system_id].items():
            if name_fragment in station_name:
                return form_factors

        return []

    def _cache_form_factors_available_at_station_id(self, system_id: str, data: dict, path: str):
        # Caches, individually per system_id, form_factors potentially available at a station, in case this is
        # deducible.
        stations = data.get('data', {}).get('stations', [])
        if isinstance(stations, list):
            form_factors_available_at_station_id = {}
            for station in stations:
                form_factors = self._deduce_form_factors_from_station(system_id, station)
                form_factors_available_at_station_id[str(station.get('station_id'))] = form_factors

            self.form_factors_available_at_station_id[system_id] = form_factors_available_at_station_id

    def _cache_form_factors_by_vehicle_type_id(self, system_id: str, data: dict, path: str):
        # cache form_factors_by_vehicle_type_id per feed
        vehicle_types = data.get('data', {}).get('vehicle_types', [])
        if isinstance(vehicle_types, list):
            self.form_factors_by_vehicle_type_id[system_id] = {
                vt['vehicle_type_id']: vt.get('form_factor', 'bicycle') for vt in vehicle_types
            }

    def _cache_free_vehicle_status(self, system_id: str, data: dict, path: str):
        # cache vehicles per feed
        vehicles = data.get('data', {}).get('bikes', data.get('vehicles', []))
        if isinstance(vehicles, list):
            self.free_vehicles_cache_per_system[system_id] = vehicles

    def _convert_station_status(self, system_id: str, data: dict, path: str) -> dict:
        if not data.get('data', {}).get('stations'):
            return data

        vehicles = self.free_vehicles_cache_per_system.get(system_id, [])
        if len(vehicles) == 0:  # _convert_free_vehicles_status has not yet been called for this system_id
            return data

        update_stations_availability_status(data['data']['stations'], vehicles)
        set_vehicle_types_available_defaults(
            data['data']['stations'],
            self.form_factors_available_at_station_id.get(system_id),
            self.form_factors_by_vehicle_type_id.get(system_id),
        )

        return data
