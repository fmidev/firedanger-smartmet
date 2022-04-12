#!/bin/env bash
eval "$(conda shell.bash hook)"
conda activate xr
cd ~/data/sen5p
echo  "$2"
if [[ "$2" == 'AER_AI' ]]
then
 v2='aerosol_index_354_388'; v='aod340'; n='total_aerosol_optical_depth_at_340'; p='217.210';
elif [[ "$2" == 'AER_LH' ]]
then
 v='aot340'; v2='aerosol_mid_pressure'; n='profile_of_optical_thickness_at_340'; p='52.214';
elif [[ "$2" == 'CLOUD_' ]]
then
 v4='cloud_optical_thickness'; v='cf'; v2='cloud_base_height'; v3='cloud_top_height'; n='cloud_area_fraction'; p='213.130';
elif [[ "$2" == 'CO____' ]]
then
 v='tco'; n='atmosphere_mass_content_of_carbon_monoxide'; p='127.210';
elif [[ "$2" == 'HCHO__' ]]
then
 v='tchcho'; n='atmosphere_mass_content_of_formaldehyde'; p='128.210';
elif [[ "$2" == 'NO2___' ]]
then
 v='tcno2'; n='atmosphere_mass_content_of_nitrogen_dioxide'; p='125.210';
elif [[ "$2" == 'O3____' ]]
then
 v='tco3'; n='atmosphere_mass_content_of_ozone'; p='206.128';
elif [[ "$2" == 'O3__PR' ]]
then
 v='o3'; n='troposhere_mole_content_of_ozone'; p='203.128';
elif [[ "$2" == 'SO2___' ]]
then
 v='tcso2'; n='atmosphere_mass_content_of_sulfur_dioxide'; p='126.210';
fi
input="-remapbil,../s5p-sam-grid"
infiles=$(ls -1 S5P_*$2_${1}T*/S5P_*[0-9]-cl.nc) 
for f in $infiles
do 
    ins+="$input $f "
done
echo $ins
#cdo --eccodes -O -f grb1 -b P12 ensmean $ins ../grib/S5P_${1:0:4}0101T000000_${1}T000000_$2.grib
cdo -s -O -f nc4c -z zip6 ensmean -setrtomiss,-1,-0.001 $ins ../nc/S5P_${1:0:4}0101T000000_${1}T000000_$2.nc
cdo -s --eccodes -f grb1 -b P12 setparam,$p -selname,$v ../nc/S5P_${1:0:4}0101T000000_${1}T000000_$2.nc ../grib/S5P_${1:0:4}0101T000000_${1}T000000_$2.grib