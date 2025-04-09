from typing import Union

from app.base_converter import BaseConverter


class GbfsSetTtlConverter(BaseConverter):
    hostnames = [
        'gbfs.nextbike.net',
        'apis.deutschebahn.com',
        'stables.donkey.bike',
        'data.lime.bike',
        'mds.bird.co',
        'gbfs.prod.sharedmobility.ch',
        'api.voiapp.io',
        'gbfs.api.ridedott.com',
    ]

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if not path.endswith(('/station_status', '/station_status.json', '/free_bike_status', '/free_bike_status.json')):
            if 'ttl' not in data or data['ttl'] == 0:
                data['ttl'] = 3600  # seconds per hour
            return data

        return data
