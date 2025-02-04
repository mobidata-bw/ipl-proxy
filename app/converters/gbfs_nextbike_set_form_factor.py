from typing import Union

from app.base_converter import BaseConverter


class GbfsNextbikeSetFormFactorConverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith('/vehicle_types.json'):
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            vehicle_types = fields.get('vehicle_types', [])
            if not isinstance(vehicle_types, list):
                return data
            for vehicle_type in vehicle_types:
                if 'form_factor' not in vehicle_type:
                    vehicle_type['form_factor'] = 'other'
                if 'propulsion_type' not in vehicle_type:
                    vehicle_type['propulsion_type'] = 'human'
            return data

        return data
