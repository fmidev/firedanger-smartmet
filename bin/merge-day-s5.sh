#!/bin/env bash
eval "$(conda shell.bash hook)"
conda activate xr
cd ~/data/sen5p
echo  "$2"
if [[ "$2" == 'AER_AI' ]]
then
 v2='aerosol_index_354_388'; v='aod340'; n='total_aerosol_optical_depth_at_340';
elif [[ "$2" == 'AER_LH' ]]
then
 v='aot340'; v2='aerosol_mid_pressure'; n='profile_of_optical_thickness_at_340';
elif [[ "$2" == 'CLOUD_' ]]
then
 v4='cloud_optical_thickness'; v='cloud_fraction'; v2='cloud_base_height'; v3='cloud_top_height'; n='cloud_area_fraction';
elif [[ "$2" == 'CO____' ]]
then
 v='tco'; n='atmosphere_mass_content_of_carbon_monoxide';
elif [[ "$2" == 'HCHO__' ]]
then
 v='tchcho'; n='atmosphere_mass_content_of_formaldehyde';
elif [[ "$2" == 'NO2___' ]]
then
 v='tcno2'; n='atmosphere_mass_content_of_nitrogen_dioxide';
elif [[ "$2" == 'O3____' ]]
then
 v='tco3'; n='atmosphere_mass_content_of_ozone';
elif [[ "$2" == 'O3__PR' ]]
then
 v='o3'; n='troposhere_mole_content_of_ozone';
elif [[ "$2" == 'SO2___' ]]
then
 v='tcs02'; n='atmosphere_mass_content_of_sulfur_dioxide';
fi
input="-remapbil,../s5p-sam-grid"
infiles=$(ls -1 S5P_*$2_${1}T*/S5P_*[0-9]-cl.nc) 
for f in $infiles
do 
    ins+="$input $f "
done
echo $ins
cdo --eccodes -O -f grb1 -b P12 chname,var1,$v -ensmean $ins ../grib/S5P_${1:0:4}0101T000000_${1}T000000_$2.grib
#cdo --eccodes -O -f nc4c ensmean $ins ../nc/S5P_${1:0:4}0101T000000_${1}T000000_$2.nc
