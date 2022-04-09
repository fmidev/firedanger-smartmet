#!/usr/bin/env python
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'seasonal-original-single-levels',
    {
        'format': 'grib',
        'originating_centre': 'ecmwf',
        'system': '5',
        'variable': 'orography',
        'year': '2018',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': '01',
        'leadtime_hour': '0',
        'area': [
            75, -30, 25,
            50,
        ],
    },
    '/home/users/smartmet/data/Annin/ec-sf_2018_orography-euro.grib')
