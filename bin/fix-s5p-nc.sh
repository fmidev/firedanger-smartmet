#!/bin/env bash
eval "$(conda shell.bash hook)"
conda activate xr
echo  "${1:13:6}"
if [[ "${1:13:6}" == 'AER_AI' ]]
then
 v2='aerosol_index_354_388'; v='aerosol_index_340_380'; n='total_aerosol_optical_depth_at_340'; s='aod340';
elif [[ "${1:13:6}" == 'AER_LH' ]]
then
 v='aerosol_mid_height'; v2='aerosol_mid_pressure'; n='profile_of_optical_thickness_at_340'; s='aot340';
elif [[ "${1:13:6}" == 'CLOUD_' ]]
then
 v4='cloud_optical_thickness'; v='cloud_fraction'; v2='cloud_base_height'; v3='cloud_top_height';
 n='cloud_area_fraction'; s='cf';
elif [[ "${1:13:6}" == 'CO____' ]]
then
 v='carbonmonoxide_total_column'; n='atmosphere_mass_content_of_carbon_monoxide'; s='tco';
elif [[ "${1:13:6}" == 'HCHO__' ]]
then
 v='formaldehyde_tropospheric_vertical_column'; n='atmosphere_mass_content_of_formaldehyde'; s='tchcho';
elif [[ "${1:13:6}" == 'NO2___' ]]
then
 v='nitrogendioxide_tropospheric_column'; n='atmosphere_mass_content_of_nitrogen_dioxide'; s='tcno2';
elif [[ "${1:13:6}" == 'O3____' ]]
then
 v='ozone_total_vertical_column'; n='atmosphere_mass_content_of_ozone'; s='tco3';
elif [[ "${1:13:6}" == 'O3__PR' ]]
then
 v='ozone_profile_subcolumns'; n='mass_fraction_of_ozone_in_air'; s='o3';
elif [[ "${1:13:6}" == 'SO2___' ]]
then
 v='sulfurdioxide_total_vertical_column'; n='atmosphere_mass_content_of_sulfur_dioxide';
 s='tcso2'
fi
#ncks -O -7 -G : -v $v,${v}_precision $1 ${1:0:-3}-cl.nc
ncks -O -7 -G : -v $v $1 ${1:0:-3}-cl.nc
ncatted -a bounds,longitude,o,c,'longitude_bounds' -a bounds,latitude,o,c,'latitude_bounds' \
 -a coordinates,"$v",o,c,'longitude latitude' -a standard_name,"$v",o,c,"$n" \
 -a short_name,"$v",a,c,"$s" ${1:0:-3}-cl.nc
 
[[ "${1:13:6}" == 'NO2___' ]] && ncatted -a coordinates,air_mass_factor_total,o,c,'longitude latitude' \
 -a coordinates,air_mass_factor_troposphere,o,c,'longitude latitude' \
 -a coordinates,averaging_kernel,o,c,'longitude latitude' \
 -a coordinates,tm5_tropopause_layer_index,o,c,'longitude latitude' \
 -a coordinates,surface_pressure,o,c,'longitude latitude' ${1:0:-3}-cl.nc
[[ "${1:13:6}" == 'O3__PR' ]] && ncatted  -a coordinates,${v}_precision,o,c,'longitude latitude' ${1:0:-3}-cl.nc
ncrename -O -v $v,$s ${1:0:-3}-cl.nc
