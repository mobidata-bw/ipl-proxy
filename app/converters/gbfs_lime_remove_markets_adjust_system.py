from typing import Union

from app.base_converter import BaseConverter


class GbfsLimeRemoveMarketsAdjustSystemConverter(BaseConverter):
    hostnames = ['data.lime.bike']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not path.startswith('/api/partners/v2/gbfs_transit/'):
            return data

        if path.endswith('/gbfs.json'):
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
                    if feed.get('name') != 'markets':
                        new_feeds.append(feed)
                fields[language]['feeds'] = new_feeds
            return data

        if path.endswith('/system_information.json'):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            fields['operator'] = 'Lime'
            fields['timezone'] = 'Europe/Berlin'
            fields['license_url'] = 'https://www.li.me/gbfs-terms'
            fields['rental_apps'] = {
                'android': {
                    'store_uri': 'https://play.google.com/store/apps/details?id=com.limebike&hl=de',
                    'discovery_uri': 'https://www.li.me/yet_unknown',
                },
                'ios': {
                    'store_uri': 'https://apps.apple.com/de/app/lime-ridegreen/id1199780189',
                    'discovery_uri': 'https://www.li.me/yet_unknown',
                },
            }
            return data

        return data
