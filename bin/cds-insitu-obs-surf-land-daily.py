import cdsapi
import sys

year=sys.argv[1]
mon=sys.argv[2]
print('/home/users/smartmet/data/Annin/insitu-obs-land-surf_daily_eu_%s%s.zip'%(year,mon))

c = cdsapi.Client()

c.retrieve(
    'insitu-observations-surface-land',
    {
        'format': 'zip',
        'time_aggregation': 'daily',
        'variable': [
            'air_pressure', 'air_temperature', 'wind_from_direction', 'wind_speed',
        ],
        'usage_restrictions': 'unrestricted',
        'data_quality': 'passed',
        'year': year,
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
        'area': [
            75, -30, 25,
            50,
        ],
        'month': mon,
    },
    '/home/users/smartmet/data/Annin/insitu-obs-land-surf_daily_eu_%s%s.zip'%(year,mon))
