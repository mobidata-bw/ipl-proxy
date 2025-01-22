from typing import List, Union

from app.base_converter import BaseConverter


class GbfsMobilityChRemoveVehicleTypesAvailableConverter(BaseConverter):
    hostnames = ['gbfs.prod.sharedmobility.ch']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not path.startswith('/v2/gbfs/mobility'):
            return data

        # remove invalid station entry: "vehicle_types_available": [ {"vehicle_type_id": "notAvailable", "count": 0} ]
        if '/station_status' in path:
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations', [])
            if not isinstance(stations, list):
                return data
            for station in stations:
                vehicle_types_available = station.get('vehicle_types_available', [])
                if not isinstance(vehicle_types_available, list):
                    continue
                for vehicle_type_available in vehicle_types_available:
                    if vehicle_type_available.get('vehicle_type_id') == 'notAvailable':
                        del station['vehicle_types_available']
                        break
            return data

        return data
