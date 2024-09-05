from typing import Union

from app.base_converter import BaseConverter


class GbfsDonkeyKreuzlingenSetCurrentRangeMetersConverter(BaseConverter):
    hostnames = ['stables.donkey.bike']

    @staticmethod
    def _get_system_id_from_path(path: str) -> str:
        return path.split('/')[-3]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        system_id = self._get_system_id_from_path(path)
        if system_id != 'donkey_kreuzlingen':
            return data

        if path.endswith('/free_bike_status.json'):
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            vehicles = fields.get('bikes', [])
            if not isinstance(vehicles, list):
                return data
            for vehicle in vehicles:
                if 'current_range_meters' in vehicle and vehicle['current_range_meters'] is None:
                    vehicle['current_range_meters'] = 1000
                if 'current_fuel_percent' in vehicle and vehicle['current_fuel_percent'] is None:
                    del vehicle['current_fuel_percent']
            return data

        return data
