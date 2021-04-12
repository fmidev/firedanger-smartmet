#!/usr/bin/env python3                                                                                                                                                     
import sys
import cdsapi

c = cdsapi.Client()
mon= sys.argv[1]
years=sys.argv[2:]
year=sys.argv[2]+'-'+sys.argv[-1]
print(years, year)

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'grib',
# euro        'area' : '75/-30/25/50',
        'area' : '-10/-80/-60/-50',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            'maximum_2m_temperature_in_the_last_24_hours','minimum_2m_temperature_in_the_last_24_hours',
            '2m_dewpoint_temperature', '2m_temperature',
            'evaporation', 'potential_evaporation', 'runoff',
            'skin_reservoir_content', 'skin_temperature',
            'snow_albedo','snow_density', 'snow_depth',
            'snow_depth_water_equivalent', 'snow_evaporation', 'snowfall',
            'snowmelt', 'soil_temperature_level_1', 'soil_temperature_level_2',
            'soil_temperature_level_3', 'soil_temperature_level_4', 'sub_surface_runoff',
            'surface_runoff', 'temperature_of_snow_layer', 'volumetric_soil_water_layer_1',
            'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'surface_pressure',
            'total_precipitation'
        ],
        'year': years,
        'month': mon,
        'time': '00:00',
    },
    '/data/era5_%s_stats_%s_sam.grib'%(year,mon))
