from typing import Union

from app.base_converter import BaseConverter


class GbfsPickebikeBaselChangePricingPlanIdConverter(BaseConverter):
    hostnames = ['gbfs.prod.sharedmobility.ch']

    def convert(self, data: Union[dict, list], path: str) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data
        if not path.startswith('/v2/gbfs/pickebike_basel'):
            return data

        if '/free_bike_status' in path:
            fields = data.get('data', {})
            if not isinstance(fields, dict):
                return data
            vehicles = fields.get('bikes', [])
            if not isinstance(vehicles, list):
                return data
            for vehicle in vehicles:
                if vehicle.get('pricing_plan_id') == 'default_':
                    vehicle['pricing_plan_id'] = 'default_' + vehicle.get('vehicle_type_id', '')
            return data

        return data
