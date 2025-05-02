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
                if path.startswith('/db-api-marketplace/apis/shared-mobility-gbfs/v2/de/RegioRadStuttgart'):
                    vehicle_type['return_constraint'] = 'any_station'
                if path.startswith('/maps/gbfs/v2/nextbike_df'):
                    vehicle_type['return_constraint'] = 'any_station'
            return data

        return data
