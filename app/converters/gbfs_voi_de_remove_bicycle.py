from typing import Union

from app.base_converter import BaseConverter


class GbfsVoiDeRemoveBicycleConverter(BaseConverter):
    """
    voi_de contains no bicycles, so we can remove all voi_bike entries.
    """

    hostnames = ['api.voiapp.io']

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
            newlist = []
            for vehicle_type in vehicle_types:
                if vehicle_type.get('vehicle_type_id') != 'voi_bike':
                    newlist.append(vehicle_type)
            fields['vehicle_types'] = newlist
            return data

        if path.endswith('/station_status.json'):
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
                newlist = []
                for vehicle_type_available in vehicle_types_available:
                    if vehicle_type_available.get('vehicle_type_id') != 'voi_bike':
                        newlist.append(vehicle_type_available)
                station['vehicle_types_available'] = newlist
            return data

        return data
