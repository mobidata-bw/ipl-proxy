# Changelog

The changelog lists relevant feature changes between each release. Search GitHub issues and pull requests for smaller issues.

## 2025-06-25:
- add converter for bolt feeds: remove all bicycle entries
  - note: if future bolt feeds contain bicycles, the bicycle entries must be added again

## 2025-05-16:
- add converter for protected lime feed: remove `markets` feed and set `rentals_apps`

## 2025-05-05:
- add converter for all feeds: set return_constraint if not defined

## 2025-04-09:
- add converter for all feeds: override ttl=0

## 2025-03-10:
- generalize lime-remove-stations converter for `data.lime.bike` and `gbfs.prod.sharedmobility.ch`

## 2025-02-03:
- chore(deps): bump mitmproxy to version 11.0.1

## 2025-01-29
- add converter for `gbfs.api.ridedott.com` feeds: adjust station attributes

## 2025-01-24
- replace converter for `gbfs.prod.sharedmobility.ch/v2/gbfs/mobility` feed: clear invalid vehicle_types_available entries instead of removing them

## 2025-01-20
- add converter for `gbfs.prod.sharedmobility.ch/v2/gbfs/mobility` feed: remove invalid vehicle_types_available entries

## 2024-12-10
- add converter for `api.voiapp.io/gbfs/v2` feed: remove all voi_bike entries

## 2024-11-12
- add converter for `gbfs.prod.sharedmobility.ch/v2/gbfs/pickebike_basel` feed: set valid pricing_plan_id

## 2024-09-17
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

