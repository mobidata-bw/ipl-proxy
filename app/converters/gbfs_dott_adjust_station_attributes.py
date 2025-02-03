from typing import List, Union

from app.base_converter import BaseConverter


class GbfsDottAdjustStationAttributesConverter(BaseConverter):
    hostnames = ['gbfs.api.ridedott.com']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        # remove station.region_id because system_regions.json is not available
        if path.endswith('/station_information.json'):
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations', [])
            if not isinstance(stations, list):
                return data
            for station in stations:
                if 'region_id' in station:
                    del station['region_id']
            return data

        # set station.is_installed and station.is_renting to true because parking space is available
        if path.endswith('/station_status.json'):
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations', [])
            if not isinstance(stations, list):
                return data
            for station in stations:
                if 'is_installed' in station:
                    station['is_installed'] = True
                if 'is_renting' in station:
                    station['is_renting'] = True
            return data

        return data
