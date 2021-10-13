#!/usr/bin/env python3
import sys
import yaml
import cdsapi
mon= sys.argv[1]
#years=sys.argv[2:]
#year=sys.argv[2]+'-'+sys.argv[-1]
year=2018
print(year, mon)

with open('/home/users/smartmet/.camsapirc', 'r') as f:
        credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])
c.retrieve(
    'cams-europe-air-quality-reanalyses',
    {
        'variable': [
            'dust', 'particulate_matter_10um', 'particulate_matter_2.5um',
            'secondary_inorganic_aerosol',
        ],
        'model': 'ensemble',
        'level': '0_m',
        'type': 'validated_reanalysis',
        'year': year,
        'month': mon,
        'format': 'zip',
    },
    'cams-eu-aq-ra_%s%s_PM.zip'%(year,mon))