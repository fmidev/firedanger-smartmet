#!/bin/bash
# voi ajaa smartmet puolelta näin: sh /home/users/kroger/firedanger-smartmet/bin/firedanger.sh 20220731
eval "$(conda shell.bash hook)"
conda activate xarray

cd /home/users/smartmet/data

day=$1 
date1=$(date -d "$day" +'%Y%m%d') 
year1=$(date -d "$date1" +%Y)
date2=$(date -d "$day - 1 day" +'%Y%m%d')
year2=$(date -d "$date2" +%Y)
date3=$(date -d "$day - 2 day" +'%Y%m%d')
year3=$(date -d "$date3" +%Y)
dateOut=$(date -d "$day + 1 day" +'%Y%m%d')
yearOut=$(date -d "$dateOut" +%Y)

#dc0file=ECFWI_20220731T120000_DC_hr_v4.0_con_latlon.grib
# jos day on 20220731, dc0file on ecfwi
# jos day ei ole 20220731, dc0file on date-1pvä era5
dc0file=ERA5_${year1}0101T000000_${date1}T120000_dc_arc.grib
vars_t_file=ERA5_${year1}0101T000000_${date1}T000000_base+soil_arc.grib
vars_t_1_file=ERA5_${year2}0101T000000_${date2}T000000_base+soil_arc.grib
sde_t_file=ERA5_${year1}0101T000000_${date1}T000000_sde_arc.grib
sde_t_1_file=ERA5_${year2}0101T000000_${date2}T000000_sde_arc.grib
sde_t_2_file=ERA5_${year3}0101T000000_${date3}T000000_sde_arc.grib

#python /home/users/kroger/firedanger-smartmet/bin/firedangerECFWI.py $day $dc0file $vars_t_file $vars_t_1_file $sde_t_file $sde_t_1_file $sde_t_2_file 
python /home/users/kroger/firedanger-smartmet/bin/firedangerERA5.py $day $dc0file $vars_t_file $vars_t_1_file $sde_t_file $sde_t_1_file $sde_t_2_file $dc_out_file

cdo --eccodes -b 16 -f grb2 copy -setparam,8.4.2 -setmissval,-99999 dc-out-${dateOut}.nc grib/ERA5_${yearOut}0101T000000_${dateOut}T120000_dc_arc.grib
rm dc-out-${dateOut}.nc

### aikaleima out tieoostojen sisällä on väärin!!! vai sekoilinko pvm kanssa nyt tässä, tarkista.. varmaan sekoilin koska dc_real on pakko olla se the pvä 
### /home/users/smartmet/data/grib/ERA5_20230101T000000_20221231T000000_base+soil_arc.grib' problem
#korjaa time slicet niin että ottaa täältä datet nihin argumentteina
# lisää output file python kutsuun ja muokkaa se gribiksi

# tee ensin se eka era5 dc tiedosto gribiksi ja sitten muokkaa firedanger.py sellaiseksi, että ottaa dc0 siitä era5 tiedostosta ja ala ajaa tätä kautta
# oikeestaan pitää olla erikseen era5 päivittäin ajava skripti näille fwi:lle
# sit erikseen joka kuun 13. tms ajava mikä ottaa sen era5 onkse sit kuun 1. vai kuun 2. mistäs se lasku sit alkaa ecsf dataa saatavilla ja mitä menneisyyteen tarvittiin
# jos on 3-day sum esim sde ehdolle... 
#python /home/users/kroger/firedanger-smartmet/bin/firedanger.py 

#sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0
