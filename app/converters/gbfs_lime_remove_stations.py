from typing import Union

from app.base_converter import BaseConverter


class GbfsLimeRemoveStationsConverter(BaseConverter):
    hostnames = ['data.lime.bike', 'gbfs.prod.sharedmobility.ch']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not path.startswith(('/api/partners/v2/gbfs/', '/v2/gbfs/lime_')):
            return data

        if path.endswith('/gbfs.json') or '/gbfs?' in path:
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            for language in fields:
                feeds = fields[language].get('feeds')
                if not isinstance(feeds, list):
                    continue
                new_feeds = []
                for feed in feeds:
                    if not isinstance(feed, dict):
                        continue
                    if feed.get('name') not in ['station_information', 'station_status']:
                        new_feeds.append(feed)
                fields[language]['feeds'] = new_feeds
            return data

        return data
