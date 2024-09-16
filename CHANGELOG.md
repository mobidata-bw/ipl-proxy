# Changelog

The changelog lists relevant feature changes between each release. Search GitHub issues and pull requests for smaller issues.

[upcoming release]

- add converter for `apis.deutschebahn.com` feeds: remove capacity attribute
- change converter for `gbfs.nextbike.net` feeds: set `propulsion_type=human` if not defined

## 2024-09-10
- add converter for `gbfs.nextbike.net` feeds: set `form_factor=other` if not defined.
- fix converter for `gbfs.nextbike.net` feeds: set `current_range_meters` only for vehicles with `propulsion_type` != `human`.

## 2024-09-03
- add converter for `stables.donkey.bike/api/public/gbfs/2/donkey_kreuzlingen` feed: override `current_range_meters` and remove `current_fuel_percent` for vehicles where these attributes are null. This is a workaround for https://github.com/DonkeyRepublic/donkey_gbfs/issues/8.

##  2024-07-05
- add converter for `gbfs.nextbike.net` feed: set `max_range_meters` and `current_range_meters` for vehicles with `propulsion_type` != `human`.
- add converter for `mds.bird.co` feed: remove `station_information`, `station_status` and `free_bike_status` feeds from gbfs.json if they are always empty.  

## 2024-06-14
- add converter for `data.lime.bike` feed: remove `station_status` and `station_information` feeds from gbfs.json, as Lime associates all free floating bikes to a single station, which is semantically wrong.

