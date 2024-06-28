from typing import List, Union

from app.base_converter import BaseConverter


class GbfsNextbikeSetRangePropertiesConverter(BaseConverter):
    hostnames = ['gbfs.nextbike.net']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith('/vehicle_types.json'):
            for vehicle_type in data['data'].get('vehicle_types', []):
                if 'propulsion_type' not in vehicle_type or vehicle_type['propulsion_type'] == 'human':
                    continue
                if 'max_range_meters' not in vehicle_type or vehicle_type['max_range_meters'] == 0:
                    vehicle_type['max_range_meters'] = 60000
            return data

        if path.endswith('/free_bike_status.json'):
            for bike in data['data'].get('bikes', []):
                if 'vehicle_type_id' not in bike:
                    continue
                # vehicle_type_id = bike['vehicle_type_id']
                # check if vehicle_type has propulsion_type != human
                if 'current_range_meters' not in bike or bike['current_range_meters'] == 0:
                    bike['current_range_meters'] = 1000
            return data

        return data
