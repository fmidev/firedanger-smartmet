#!/bin/bash
#
# Fetching global Fire danger indices historical data (CEMS) from cdsapi 
# and setting it up in the smartmet-server
#
# 2023 Anni Kröger
# sh /home/users/kroger/firedanger-smartmet/bin/get-fire-daily.sh

eval "$(conda shell.bash hook)"
#source ~/.smart # arctic domain
if [ $# -ne 0 ]
then
    year=$1
    month=$2
    day=$3
else
    year=$(date -d '6 days ago' +%Y)
    month=$(date -d '6 days ago' +%m)
    day=$(date -d '6 days ago' +%d)
fi
cd /home/users/smartmet/data
echo "fetch ECFWI for y: $year m: $month d: $day"
[ -f ECFWI_$year$month${day}T000000_daily_v4-1.grib ] || /home/users/smartmet/firedanger-smartmet/bin/cds-ecfwi.py $year $month $day
conda activate xarray

## move og to grib/
mv ECFWI_$year$month${day}T000000_daily_v4-1.grib grib/

#sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0
