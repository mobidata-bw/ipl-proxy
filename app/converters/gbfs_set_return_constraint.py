from typing import Union

from app.base_converter import BaseConverter


class GbfsSetReturnConstraintConverter(BaseConverter):
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
        'www.share-birrer.ch',
        'auto-birrer.ch',
    ]

    # ensure that return_constraint is always set
    # this attribute is necessary for intermodal routing
    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith(('/vehicle_types', '/vehicle_types.json')):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            vehicle_types = fields.get('vehicle_types')
            if not isinstance(vehicle_types, list):
                return data
            for vehicle_type in vehicle_types:
                if 'return_constraint' in vehicle_type:
                    continue
                if vehicle_type.get('form_factor', '') == 'bicycle':
                    vehicle_type['return_constraint'] = 'any_station'  # valid for most providers
                if vehicle_type.get('form_factor', '') == 'scooter':
                    vehicle_type['return_constraint'] = 'free_floating'  # valid for most providers
                if path.startswith('/maps/gbfs/v2/nextbike_fg'):
                    vehicle_type['return_constraint'] = 'hybrid'
                if path.startswith('/public/v2/'):  # dott feed
                    vehicle_type['return_constraint'] = 'hybrid'
            return data

        return data
