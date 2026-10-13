from typing import Union

from app.base_converter import BaseConverter


class GbfsRemoveStationsConverter(BaseConverter):
    hostnames = [
        'zeus.rideatom.com',
        'yoio.rideatom.com',
    ]

    # remove empty station_information/station_status feeds
    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith(('/gbfs', '/gbfs.json')) or '/gbfs?' in path:
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            feeds = fields.get('feeds')
            if not isinstance(feeds, list):
                return data
            new_feeds = []
            for feed in feeds:
                if not isinstance(feed, dict):
                    continue
                if feed.get('name') not in ['station_information', 'station_status']:
                    new_feeds.append(feed)
            fields['feeds'] = new_feeds
            return data

        return data
