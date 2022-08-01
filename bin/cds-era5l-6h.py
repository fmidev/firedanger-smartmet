#!/usr/bin/python3
import cdsapi
import sys

year= sys.argv[1]
print('/home/users/smartmet/data/era5l-%s-sl-6h-euro.grib'%year)

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land',
    {
        'format': 'grib',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
            '2m_temperature', 'evaporation_from_bare_soil', 'evaporation_from_open_water_surfaces_excluding_oceans',
            'evaporation_from_the_top_of_canopy', 'evaporation_from_vegetation_transpiration', 'forecast_albedo',
            'potential_evaporation', 'runoff', 'skin_reservoir_content',
            'skin_temperature', 'snow_albedo', 'snow_cover',
            'snow_density', 'snow_depth', 'snow_depth_water_equivalent',
            'snow_evaporation', 'snowfall', 'snowmelt',
            'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
            'soil_temperature_level_4', 'sub_surface_runoff', 'surface_latent_heat_flux',
            'surface_net_solar_radiation', 'surface_net_thermal_radiation', 'surface_pressure',
            'surface_runoff', 'surface_sensible_heat_flux', 'surface_solar_radiation_downwards',
            'surface_thermal_radiation_downwards', 'temperature_of_snow_layer', 'total_evaporation',
            'total_precipitation', 'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
            'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
        ],
        'year': year,
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '06:00', '12:00',
            '18:00',
        ],
        'area': [
            75, -30, 25,
            50,
        ],
    },
    '/home/users/smartmet/data/era5l-%s-6h-euro.grib'%year)
