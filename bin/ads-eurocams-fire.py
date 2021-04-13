#!/usr/bin/env python3
import sys
import cdsapi
if ( len(sys.argv) > 2):
    year= sys.argv[1]
    month= sys.argv[2]
    day= sys.argv[3]

with open('/home/users/smartmet/.camsapirc', 'r') as f:
        credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])
c.retrieve(
    'cams-europe-air-quality-forecasts',
    {
        'variable': 'pm10_wildfires',
        'model': 'ensemble',
        'level': '0',
        'date': '%s-%s-01/%s-%s-%s' % (year,month,year,month,day),
        'type': ['analysis','forecast'],
        'time': [ '00:00', '12:00', ],
        'leadtime_hour': ['0','12', '24','36', '48', '60','72', '84', '96'],
        'format': 'grib',
    },
    '/home/smartmet/data/grib/CAMSE_%s%s01T0000_%s%s%s_WFPM10_12h.grib' % (year,month,year,month,day))