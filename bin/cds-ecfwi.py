import cdsapi
import sys

c = cdsapi.Client()
year=sys.argv[1]
month=sys.argv[2]
day=sys.argv[3]

c.retrieve(
    'cems-fire-historical-v1',
    {
        'product_type': 'reanalysis',
        'variable': [
            'build_up_index', 'drought_code', 'duff_moisture_code',
            'fine_fuel_moisture_code', 'fire_daily_severity_rating', 'fire_weather_index',
            'initial_fire_spread_index',
        ],
        'dataset_type': 'intermediate_dataset',
        'system_version': '4_1',
        'year': year,
        'month': month,
        'day': day,
        'grid': 'original_grid',
        'format': 'grib',
    },
    '/home/users/smartmet/data/ECFWI_%s%s%sT000000_daily_v4-1.grib'%(year,month,day))