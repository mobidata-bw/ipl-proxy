# Changelog

The changelog lists relevant feature changes between each release. Search GitHub issues and pull requests for smaller issues.

## Upcoming release (under development)
-

##  2024-07-05
- add converter for `gbfs.nextbike.net` feed: set `max_range_meters` and `current_range_meters` for vehicles with `propulsion_type` != `human`.
- add converter for `mds.bird.co` feed: remove `station_information`, `station_status` and `free_bike_status` feeds from gbfs.json if they are always empty.  

## 2024-06-14
- add converter for `data.lime.bike` feed: remove `station_status` and `station_information` feeds from gbfs.json, as Lime associates all free floating bikes to a single station, which is semantically wrong.

