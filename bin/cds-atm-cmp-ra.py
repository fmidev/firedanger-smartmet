#!/usr/bin/env python3
import sys
import yaml
import cdsapi

with open('/home/users/smartmet/.camsapirc', 'r') as f:
        credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])
c.retrieve(
    'cams-global-reanalysis-eac4-monthly',
    {
        'format': 'grib',
        'variable': [
            '2m_dewpoint_temperature', '2m_temperature', 'black_carbon_aerosol_optical_depth_550nm',
            'charnock', 'dust_aerosol_optical_depth_550nm', 'ice_temperature_layer_1',
            'leaf_area_index_high_vegetation', 'leaf_area_index_low_vegetation', 'mean_sea_level_pressure',
            'organic_matter_aerosol_optical_depth_550nm', 'particulate_matter_10um', 'particulate_matter_2.5um',
            'sea_ice_cover', 'sea_salt_aerosol_optical_depth_550nm', 'sea_surface_temperature',
            'snow_albedo', 'snow_density', 'snow_depth',
            'soil_temperature_level_1', 'sulphate_aerosol_optical_depth_550nm', 'surface_pressure',
            'temperature_of_snow_layer', 'total_aerosol_optical_depth_550nm', 'total_column_carbon_monoxide',
            'total_column_ethane', 'total_column_formaldehyde', 'total_column_hydroxyl_radical',
            'total_column_isoprene', 'total_column_methane', 'total_column_nitric_acid',
            'total_column_nitrogen_dioxide', 'total_column_nitrogen_monoxide', 'total_column_ozone',
            'total_column_peroxyacetyl_nitrate', 'total_column_propane', 'total_column_sulphur_dioxide',
            'total_column_water', 'total_column_water_vapour', 'vertically_integrated_mass_of_dust_aerosol_0.03-0.55um',
            'vertically_integrated_mass_of_dust_aerosol_0.55-9um', 'vertically_integrated_mass_of_dust_aerosol_9-20um', 'vertically_integrated_mass_of_hydrophilic_black_carbon_aerosol',
            'vertically_integrated_mass_of_hydrophilic_organic_matter_aerosol', 'vertically_integrated_mass_of_hydrophobic_black_carbon_aerosol', 'vertically_integrated_mass_of_hydrophobic_organic_matter_aerosol',
            'vertically_integrated_mass_of_sea_salt_aerosol_0.03-0.5um', 'vertically_integrated_mass_of_sea_salt_aerosol_0.5-5um', 'vertically_integrated_mass_of_sea_salt_aerosol_5-20um',
            'vertically_integrated_mass_of_sulphate_aerosol', 'vertically_integrated_mass_of_sulphur_dioxide',
        ],
        'year': [
            '2003', '2004', '2005',
            '2006', '2007', '2008',
            '2009', '2010', '2011',
            '2012', '2013', '2014',
            '2015', '2016', '2017',
            '2018', '2019', '2020',
        ],
        'product_type': 'monthly_mean_by_hour_of_day',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'time': [
            '00:00', '03:00', '06:00',
            '09:00', '12:00', '15:00',
            '18:00', '21:00',
        ],
        'area': [
            -10, -80, -60,
            -50,
        ],
    },
    '/data/eac4-monthly-hourly.grib')