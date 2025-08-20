from typing import Union

from app.base_converter import BaseConverter

BICYCLE_ELECTRIC_MAX_RANGE_METERS = 60000


class GbfsShareBirrerAdjustBicycleConverter(BaseConverter):
    """
    share_birrer_ch uses invalid form_factor 'bike'
    """

    hostnames = ['www.share-birrer.ch']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        if path.endswith('/vehicle_types'):
            fields = data.get('data')
            if not isinstance(fields, dict):
                return data
            vehicle_types = fields.get('vehicle_types')
            if not isinstance(vehicle_types, list):
                return data
            for vehicle_type in vehicle_types:
                if vehicle_type.get('form_factor') == 'bike':
                    vehicle_type['form_factor'] = 'bicycle'
                    vehicle_type['propulsion_type'] = 'electric'
                    vehicle_type['max_range_meters'] = BICYCLE_ELECTRIC_MAX_RANGE_METERS
            return data

        return data
