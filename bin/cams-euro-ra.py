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
            'ammonia', 'carbon_monoxide', 'nitrogen_dioxide',
            'nitrogen_monoxide', 'non_methane_vocs', 'ozone',
            'peroxyacyl_nitrates', 'sulphur_dioxide',
        ],
        'model': 'ensemble',
        'level': '0_m',
        'type': 'validated_reanalysis',
        'year': '2018',
        'month': '01',
        'format': 'zip',
    },
    'cams-eu-aq-ra_%s%s_gas.zip'%(year,mon))