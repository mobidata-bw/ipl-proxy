"""
MobiData BW Proxy
Copyright (c) 2023, systect Holger Bruch
All rights reserved.
"""

from typing import Union

from app.base_converter import BaseConverter


class GbfsHttpsToHttpConverter(BaseConverter):
    hostnames = [
        'gbfs.nextbike.net',
        'apis.deutschebahn.com',
        'stables.donkey.bike',
        'data.lime.bike',
        'mds.bird.co',
        'gbfs.prod.sharedmobility.ch',
        'api.voiapp.io',
        'gbfs.api.ridedott.com',
        'zeus.city',
        'yoio.rideatom.com',
    ]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not (path.endswith(('/gbfs.json', '/gbfs'))):
            return data

        if not isinstance(data, dict) or 'data' not in data or not isinstance(data['data'], dict):
            return data

        for language in data['data']:
            if 'feeds' not in data['data'][language] or not isinstance(data['data'][language]['feeds'], list):
                continue
            for feed in data['data'][language]['feeds']:
                if not isinstance(feed, dict) or 'url' not in feed or not isinstance(feed['url'], str):
                    continue
                feed['url'] = f'http{feed["url"][5:]}'

        return data
