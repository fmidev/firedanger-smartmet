import cdsapi
import sys 

year= sys.argv[1]
mon= sys.argv[2]
day= sys.argv[3]
date='%s-%s-%s'%(year,mon,day)

c = cdsapi.Client()

c.retrieve(
    'cams-global-atmospheric-composition-forecasts',
    {
        'variable': [
            'ammonium_aerosol_mass_mixing_ratio', 'carbon_monoxide', 'dust_aerosol_0.03-0.55um_mixing_ratio',
            'dust_aerosol_0.55-0.9um_mixing_ratio', 'dust_aerosol_0.9-20um_mixing_ratio', 'ethane',
            'formaldehyde', 'hydrogen_peroxide', 'hydrophilic_black_carbon_aerosol_mixing_ratio',
            'hydrophilic_organic_matter_aerosol_mixing_ratio', 'hydrophobic_black_carbon_aerosol_mixing_ratio', 'hydrophobic_organic_matter_aerosol_mixing_ratio',
            'hydroxyl_radical', 'isoprene', 'methane',
            'nitrate_coarse_mode_aerosol_mass_mixing_ratio', 'nitrate_fine_mode_aerosol_mass_mixing_ratio', 'nitric_acid',
            'nitrogen_dioxide', 'nitrogen_monoxide', 'ozone',
            'peroxyacetyl_nitrate', 'propane', 'sea_salt_aerosol_0.03-0.5um_mixing_ratio',
            'sea_salt_aerosol_0.5-5um_mixing_ratio', 'sea_salt_aerosol_5-20um_mixing_ratio', 'sulphate_aerosol_mixing_ratio',
            'sulphur_dioxide',
        ],
        'pressure_level': [
            '925', '950', '1000',
        ],
        'date': '%s-%s-%s/%s-%s-%s'%(year,mon,day,year,mon,day),
        'time': [
            '00:00', '12:00',
        ],
        'leadtime_hour': [
            '0', '102', '108',
            '114', '12', '120',
            '15', '18', '21',
            '24', '3', '30',
            '36', '42', '48',
            '54', '6', '60',
            '66', '72', '78',
            '84', '9', '90',
            '96',
        ],
        'type': 'forecast',
        'area': [
            -10, -80, -60,
            -50,
        ],
        'format': 'grib',
    },
    '/data/cams-fc-%s%s%s-sam.grib'%(year,mon,day))
