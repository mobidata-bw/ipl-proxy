"""
MobiData BW Proxy
Copyright (c) 2023, systect Holger Bruch
All rights reserved.
"""

from typing import Union

from app.base_converter import BaseConverter


class GbfsHttpsToHttpConverter(BaseConverter):
    """
    This Converter rewrites the https-protocol of
    all feeds' gbfs files to http, so that subsequent
    requests of these will be handled by the proxy as well,
    which responds to http requests but not https.

    It supports GBFSv2 and GBFSv3 format.
    """

    hostnames = [
        'gbfs.nextbike.net',
        'apis.deutschebahn.com',
        'stables.donkey.bike',
        'data.lime.bike',
        'mds.bird.co',
        'mds.bolt.eu',
        'gbfs.prod.sharedmobility.ch',
        'api.voiapp.io',
        'gbfs.api.ridedott.com',
        'zeus.city',
        'yoio.rideatom.com',
        'www.share-birrer.ch',
        'auto-birrer.ch',
    ]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        def rewrite_https_to_http_for_all_feeds(feeds: list[dict]) -> None:
            for feed in feeds:
                if (
                    not isinstance(feed, dict)
                    or 'url' not in feed
                    or not isinstance(feed['url'], str)
                    or not feed['url'].startswith('https')
                ):
                    continue
                feed['url'] = f'http{feed["url"][5:]}'

        if not isinstance(data, dict):
            return data
        if not (path.endswith(('/gbfs.json', '/gbfs'))):
            return data

        if not isinstance(data, dict) or 'data' not in data or not isinstance(data['data'], dict):
            return data

        if isinstance(data['data'].get('feeds'), list):
            # this gbfs file is >= v3
            rewrite_https_to_http_for_all_feeds(data['data']['feeds'])
        else:
            for language in data['data']:
                if 'feeds' not in data['data'][language] or not isinstance(data['data'][language]['feeds'], list):
                    continue
                rewrite_https_to_http_for_all_feeds(data['data'][language]['feeds'])

        return data
