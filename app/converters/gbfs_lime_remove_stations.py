"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from typing import Union

from app.base_converter import BaseConverter


class GbfsLimeRemoveStationsConverter(BaseConverter):
    hostnames = ['data.lime.bike']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not path.endswith('/gbfs.json') or not isinstance(data, dict) or not isinstance(data.get('data'), dict):
            return data

        for language in data['data']:
            new_feeds = []
            if not isinstance(data['data'][language].get('feeds'), list):
                continue

            for feed in data['data'][language]['feeds']:
                if not isinstance(feed, dict) or feed.get('name') in ['station_information', 'station_status']:
                    continue

                new_feeds.append(feed)

            data['data'][language]['feeds'] = new_feeds

        return data
