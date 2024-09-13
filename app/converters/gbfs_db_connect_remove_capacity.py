from typing import List, Union

from app.base_converter import BaseConverter


class GbfsDbConnectRemoveCapacityConverter(BaseConverter):
    hostnames = ['apis.deutschebahn.com']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith('/station_information.json'):
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            stations = fields.get('stations', [])
            if not isinstance(stations, list):
                return data
            for station in stations:
                if 'capacity' in station:
                    del station['capacity'] # remove default value 40
            return data

        return data
