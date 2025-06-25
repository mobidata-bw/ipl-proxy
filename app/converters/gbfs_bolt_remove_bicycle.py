from typing import Union

from app.base_converter import BaseConverter


class GbfsBoltRemoveBicycleConverter(BaseConverter):
    """
    bolt contains no bicycles, so we can remove all bicycle entries.
    """

    hostnames = ['mds.bolt.eu', 'gbfs.prod.sharedmobility.ch']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not path.startswith(('/gbfs/2/', '/v2/gbfs/bolt_')):
            return data

        if path.endswith('/vehicle_types'):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            vehicle_types = fields.get('vehicle_types')
            if not isinstance(vehicle_types, list):
                return data
            newlist = []
            for vehicle_type in vehicle_types:
                if vehicle_type.get('form_factor') != 'bicycle':
                    newlist.append(vehicle_type)
            fields['vehicle_types'] = newlist
            return data

        return data
