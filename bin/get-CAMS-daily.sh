#!/bin/env bash
#
# monthly script for fetching CAMS forecast data from cdsapi, cutting out the Nordic domain
# and setting it up in the smartmet-server
#
# 11.4.2021 Mikko Strahlendorff
eval "$(conda shell.bash hook)"
if [ $# -ne 0 ]
then
    year=$1
    month=$2
    day=$3
else
    year=$(date +%Y)
    month=$(date +%m)
    day=$(date +%d)
fi
cd /data
echo "fetch CAMS for y: $year m: $month d: $day"
[ -f cams-fc-$year$month${day}-sam.grib ] || /home/users/smartmet/bin/cds-atm-cmp-fc.py $year $month $day &&\
 mv cams-fc-$year$month${day}-sam.grib grib/CAMS_$year$month${day}T000000_sfc-daily-fc-sam.grib # && \
# sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0
#/home/users/smartmet/anaconda3/envs/xr/bin/cdo --eccodes aexprf,ec-sde.instr CAMS_$year$month${day}T000000_base+soil-sam.grib grib/CAMS_${year}0101T000000_$year$month${day}T0000_base+soil-sam.grib
#rm cams_$year$month${day}-sam.grib
