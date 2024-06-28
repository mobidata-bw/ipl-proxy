from typing import List, Union

from app.base_converter import BaseConverter


class GbfsBirdRemoveStationsOrVehiclesConverter(BaseConverter):
    hostnames = ['mds.bird.co']

    @staticmethod
    def _get_system_id_from_path(path: str) -> str:
        return path.split('/')[-3:-2][0]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not path.endswith('/gbfs.json') or not isinstance(data, dict) or not isinstance(data.get('data'), dict):
            return data

        system_id = self._get_system_id_from_path(path)
        for language in data['data']:
            if not isinstance(data['data'][language].get('feeds'), list):
                continue

            new_feeds = []
            for feed in data['data'][language]['feeds']:
                if not isinstance(feed, dict):
                    continue
                if system_id in ['basel', 'biel', 'kloten', 'zurich'] and feed.get('name') in ['station_information', 'station_status']:
                    continue
                if system_id in ['sarreguemines'] and feed.get('name') in ['free_bike_status']:
                    continue
                new_feeds.append(feed)

            data['data'][language]['feeds'] = new_feeds

        return data
