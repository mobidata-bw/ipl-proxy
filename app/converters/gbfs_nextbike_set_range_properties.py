from typing import List, Union

from app.base_converter import BaseConverter


class GbfsNextbikeSetRangePropertiesConverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    vehicle_types_cache_per_system: dict[str, list[dict]] = {}

    @staticmethod
    def _get_system_id_from_path(path: str) -> str:
        return path.split('/')[-3:-2][0]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith('/vehicle_types.json'):
            vehicle_types = data.get('data', {}).get('vehicle_types', [])
            if not isinstance(vehicle_types, list):
                return data
            for vehicle_type in vehicle_types:
                if 'propulsion_type' not in vehicle_type or vehicle_type['propulsion_type'] == 'human':
                    continue
                if 'max_range_meters' not in vehicle_type:
                    vehicle_type['max_range_meters'] = 60000
            system_id = self._get_system_id_from_path(path)
            self.vehicle_types_cache_per_system[system_id] = vehicle_types
            return data

        if path.endswith('/free_bike_status.json'):
            system_id = self._get_system_id_from_path(path)
            vehicle_types = self.vehicle_types_cache_per_system.get(system_id, [])
            if not vehicle_types:
                return data
            vehicles = data.get('data', {}).get('bikes', [])
            if not isinstance(vehicles, list):
                return data
            for vehicle in vehicles:
                if 'vehicle_type_id' not in vehicle:
                    continue
                vehicle_type_id = vehicle['vehicle_type_id']
                for vehicle_type in vehicle_types:
                    if vehicle_type.get('vehicle_type_id') != vehicle_type_id:
                        continue
                    if 'max_range_meters' in vehicle_type and 'current_range_meters' not in vehicle:
                        vehicle['current_range_meters'] = 1000
                    break
            return data

        return data
