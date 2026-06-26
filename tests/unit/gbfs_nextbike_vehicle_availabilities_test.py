import copy

from app.converters.gbfs_nextbike_vehicle_availabilities import GbfsNextbikeVehicleAvailabilityConverter

vehicle_types = {
    'data': {
        'vehicle_types': [
            {'vehicle_type_id': 'a_bicycle', 'form_factor': 'bicycle'},
            {'vehicle_type_id': 'a_cargo_bicycle', 'form_factor': 'cargo_bicycle'},
        ]
    }
}

station_information = {
    'data': {
        'stations': [
            {'station_id': 'station_1', 'name': 'Station 1 RAD Station'},
            {'station_id': 'station_2', 'name': 'Station 2 PLUS Station'},
            {'station_id': 'station_3', 'name': 'Station 3 HEIMAT Station'},
            {'station_id': 'station_4', 'name': 'Station 4'},
            {'station_id': 'station_5', 'name': 'Station 5'},
        ]
    }
}


free_bike_status = {
    'data': {
        'bikes': [
            {'bike_id': 'any_id', 'is_reserved': False, 'is_disabled': False, 'vehicle_type_id': 'a_bicycle', 'station_id': 'station_5'},
        ]
    }
}


station_status = {
    'data': {
        'stations': [
            {
                'station_id': 'station_1',
            },
            {
                'station_id': 'station_2',
            },
            {
                'station_id': 'station_3',
            },
            {
                'station_id': 'station_4',
            },
            {
                'station_id': 'station_5',
            },
        ]
    }
}

converted_station_status = {
    'data': {
        'stations': [
            {'station_id': 'station_1', 'vehicle_types_available': [{'vehicle_type_id': 'a_bicycle', 'count': 0}]},
            {
                'station_id': 'station_2',
                'vehicle_types_available': [
                    {'vehicle_type_id': 'a_bicycle', 'count': 0},
                    {'vehicle_type_id': 'a_cargo_bicycle', 'count': 0},
                ],
            },
            {'station_id': 'station_3', 'vehicle_types_available': [{'vehicle_type_id': 'a_cargo_bicycle', 'count': 0}]},
            {'station_id': 'station_4', 'vehicle_types_available': [{'vehicle_type_id': 'a_bicycle', 'count': 0}]},
            {
                'station_id': 'station_5',
                'num_bikes_available': 1,
                'vehicle_types_available': [{'vehicle_type_id': 'a_bicycle', 'count': 1}],
            },
        ]
    }
}


def test_converter():
    converter = GbfsNextbikeVehicleAvailabilityConverter()
    result = converter.convert(copy.deepcopy(vehicle_types), '/maps/gbfs/v2/nextbike_kk/en/vehicle_types.json')
    assert result == vehicle_types
    result = converter.convert(copy.deepcopy(station_information), '/maps/gbfs/v2/nextbike_kk/en/station_information.json')
    assert result == station_information
    result = converter.convert(copy.deepcopy(free_bike_status), '/maps/gbfs/v2/nextbike_kk/en/free_bike_status.json')
    assert result == free_bike_status
    result = converter.convert(copy.deepcopy(station_status), '/maps/gbfs/v2/nextbike_kk/en/station_status.json')
    assert result == converted_station_status
