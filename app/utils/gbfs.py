"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""
from typing import List

def filter_duplicate_vehicle_types(data: dict) -> dict:
    if not data.get('data', {}).get('vehicle_types'):
        return data
    
    known_ids: List[str] = []
    filtered_vehicle_types: List[dict] = []

    for vehicle_type in data['data']['vehicle_types']:
        if vehicle_type.get('vehicle_type_id') in known_ids:
            continue
        known_ids.append(vehicle_type.get('vehicle_type_id'))
        filtered_vehicle_types.append(vehicle_type)

    data['data']['vehicle_types'] = filtered_vehicle_types
    return data

def add_missing_max_range_meters(data: dict, max_range_meters: int) -> dict:
    if not data.get('data', {}).get('vehicle_types'):
        return data

    for vehicle_type in data.get('data', {}).get('vehicle_types'):
        propulsion_type = vehicle_type.get('propulsion_type')
        if propulsion_type is not None and propulsion_type != 'human':
            if 'max_range_meters' not in vehicle_type:
                # TODO this should take vehicle_type_id into account
                vehicle_type['max_range_meters'] = max_range_meters
                # TODO log extension for this vehicle_type
