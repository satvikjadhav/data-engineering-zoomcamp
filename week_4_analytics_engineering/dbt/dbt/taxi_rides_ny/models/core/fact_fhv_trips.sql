{{ config(materialized='table') }}



with fhv_trips_data as (
    select *, 
        'fhv' as service_type
    from {{ ref('stg_fhv_tripdata') }}
), 

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select 
    fhv_trips_data.tripid, 
    fhv_trips_data.dispatching_base_num, 
    fhv_trips_data.pickup_locationid,
    fhv_trips_data.dropoff_locationid, 
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    fhv_trips_data.sr_flag,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    fhv_trips_data.pickup_datetime, 
    fhv_trips_data.dropoff_datetime

from fhv_trips_data
inner join dim_zones as pickup_zone
on fhv_trips_data.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_trips_data.dropoff_locationid = dropoff_zone.locationid