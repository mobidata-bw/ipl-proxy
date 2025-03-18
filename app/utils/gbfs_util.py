"""
MobiData BW Proxy
Copyright (c) 2023, systect Holger Bruch
All rights reserved.
"""

import logging
from collections import Counter
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger('utils.gbfs_utils')


def update_stations_availability_status(station_status: List[Dict], vehicles: List[Dict]) -> None:
    """
    Updates station_status' vehicle_types_available and num_bikes_available.
    A vehicle_type is available at a station, when any vehicle of it's type
    is assigned to this station. However, for the availabilty count,
    only those vehicles not reserved and not disabled are taken into account.
    """

    status_map = {station['station_id']: station for station in station_status}
    station_vehicle_type_free_cnt = _count_vehicle_types_at_station(
        vehicles, lambda v: not v['is_reserved'] and not v['is_disabled'] and 'station_id' in v
    )
    station_vehicle_type_cnt = _count_vehicle_types_at_station(vehicles, lambda v: 'station_id' in v)

    vehicle_types_per_station: Dict[str, list] = {}
    for station_vehicle_type in station_vehicle_type_cnt:
        station_id = station_vehicle_type[0]

        if station_id not in vehicle_types_per_station:
            vehicle_types_per_station[station_id] = []

        vehicle_types_per_station[station_id].append(
            {
                'vehicle_type_id': station_vehicle_type[1],
                'count': station_vehicle_type_free_cnt.get(station_vehicle_type, 0),
            }
        )

    for station_id in vehicle_types_per_station.keys():
        if station_id in status_map:
            _update_station_availability_status(vehicle_types_per_station[station_id], status_map[station_id])

    default_vehicle_types_available = [{'vehicle_type_id': vehicles[0]['vehicle_type_id'], 'count': 0}]
    for station in station_status:
        if 'vehicle_types_available' not in station:
            station['vehicle_types_available'] = default_vehicle_types_available


def _count_vehicle_types_at_station(vehicles: list[dict[str, Any]], filter: Callable[[dict], bool]) -> Counter:
    """
    Count vehicle's per vehicle_type and station, which fulfill the filter critera.
    """
    filtered_vehicle_map = {v['bike_id']: v for v in vehicles if filter(v)}
    station_vehicle_type_arr = [(v['station_id'], v['vehicle_type_id']) for v in filtered_vehicle_map.values()]

    return Counter(station_vehicle_type_arr)


def _update_station_availability_status(vt_available: List[Dict[str, Any]], station_status: Dict[str, Any]) -> None:
    """
    Sets station_status.vehicle_types_available and
    calculates num_bikes_available as the sum of all vehicle_types_available.
    Retains pre-existing vehicle_types_available (usually having count 0)
    for vehicle_type_ids without available vehicles,
    as this is the only way to find out, if vehicles are for rent at this station.
    """
    num_bikes_available = sum([vt['count'] for vt in vt_available])
    if 'num_bikes_available' in station_status:
        if num_bikes_available != station_status['num_bikes_available']:
            logger.warn(
                f'Official num_bikes_available ({station_status["num_bikes_available"]}) does not match count deduced '
                f'from vehicle_types_available ({num_bikes_available}) at station {station_status["station_id"]}'
            )
    else:
        station_status['num_bikes_available'] = num_bikes_available

    station_status['vehicle_types_available'] = _merge_vehicle_types_available(vt_available, station_status.get('vehicle_types_available'))


def _merge_vehicle_types_available(
    vt_available: List[Dict[str, Any]], pre_existing_vt: Optional[List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """
    Merges vehicle_types_available lists.
    """
    if not pre_existing_vt:
        return vt_available

    # convert both to map, merge, reconvert to list
    vt_map = {vt['vehicle_type_id']: vt for vt in vt_available}
    vt_map_fallback = {vt['vehicle_type_id']: vt for vt in pre_existing_vt}
    vt_merged = {**vt_map_fallback, **vt_map}
    return list(vt_merged.values())
