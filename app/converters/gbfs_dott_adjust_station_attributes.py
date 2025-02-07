from typing import Union

from app.base_converter import BaseConverter


class GbfsDottAdjustStationAttributesConverter(BaseConverter):
    hostnames = ['gbfs.api.ridedott.com']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        # remove station.region_id because system_regions.json is not available
        if path.endswith('/station_information.json'):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations')
            if not isinstance(stations, list):
                return data
            for station in stations:
                if 'region_id' in station:
                    del station['region_id']
            return data

        # set station.is_installed and station.is_renting to true because parking space is available
        # calculate station.num_bikes_available based on vehicle_types_available because it is always 0
        if path.endswith('/station_status.json'):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations')
            if not isinstance(stations, list):
                return data
            for station in stations:
                if 'is_installed' in station:
                    station['is_installed'] = True
                if 'is_renting' in station:
                    station['is_renting'] = True
                vehicle_types_available = station.get('vehicle_types_available')
                if not isinstance(vehicle_types_available, list):
                    continue
                num_bikes_available = 0
                for vehicle_type_available in vehicle_types_available:
                    count = vehicle_type_available.get('count')
                    if not isinstance(count, int):
                        continue
                    num_bikes_available += count
                station['num_bikes_available'] = num_bikes_available
            return data

        return data
