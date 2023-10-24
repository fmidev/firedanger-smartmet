import xarray as xr
import cfgrib
import requests
import pandas as pd
import numpy as np
import time, sys
import fireindices as fidx
import csv
from datetime import datetime,timedelta
startTime=time.time()
######################
# era5l mut eri grid
# utc to lst per lon!!!!!!!!! slice aina alueet ensin?
# t celcius
# tp in mm
# sde raja-arvo 
# lsm ehto saattaa kadottaa olemassaolevia dc arvoja?
# -> ensin tarkista onko edellinen arvo nan 
# -> sitten tarkista onko nan koska sde
# -> sitten tarkista onko nan koska lsm, pitää ehkä muuttaa raja-arvo pienemmäksi? 0? 
######################
#hello
grib_path='/home/users/smartmet/data/grib/'
path='/home/users/smartmet/data/'
t='20220731'
mon=7
t_0 = datetime.strptime(t, '%Y%m%d').date()
t_1=t_0-timedelta(days=1)
t_1_name=str(t_1).replace('-','')
t_2=t_0-timedelta(days=2)
t_2_name=(str(t_2).replace('-',''))

dc_file='ECFWI_20220731T120000_DC_hr_v4.0_con_latlon.grib'
#dc_t_1_file='ERA5_20220101T000000_20220731T120000_DC_arc.grib'

vars_t_file='ERA5_20220101T000000_'+t+'T000000_base+soil_arc.grib'
vars_t_1_file='ERA5_20220101T000000_'+t_1_name+'T000000_base+soil_arc.grib'
sde_t_file='ERA5_20220101T000000_'+t+'T000000_sde_arc.grib'
sde_t_1_file='ERA5_20220101T000000_'+t_1_name+'T000000_sde_arc.grib'
sde_t_2_file='ERA5_20220101T000000_'+t_2_name+'T000000_sde_arc.grib'

vars_t = xr.open_dataset(grib_path+vars_t_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('verifying_time','valid_time'),indexpath=''))
sde_t = xr.open_dataset(grib_path+sde_t_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('verifying_time','valid_time'),indexpath=''))
vars_t_1 = xr.open_dataset(grib_path+vars_t_1_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('verifying_time','valid_time'),indexpath=''))
sde_t_1 = xr.open_dataset(grib_path+sde_t_1_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('verifying_time','valid_time'),indexpath=''))
sde_t_2 = xr.open_dataset(grib_path+sde_t_2_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('verifying_time','valid_time'),indexpath=''))

# daily mean sde -> 3 day sum 
sde=xr.concat([sde_t_2,sde_t_1,sde_t],dim='valid_time')
sde=sde.to_dataframe()
sde_mean = sde.groupby(['latitude', 'longitude', pd.Grouper(freq='24H',level='valid_time')])['sde'].mean().reset_index(name='daily-mean-sde')
sde_mean = sde_mean.set_index(['valid_time','latitude','longitude'])
sde_sum = sde_mean.groupby(['latitude', 'longitude'])['daily-mean-sde'].sum().reset_index(name='sdesum')

era5=xr.concat([vars_t_1,vars_t],dim='valid_time')

# 24h precipitation accumulation (12:00:00UTC - 12:00:00UTC)
tp_all=era5.sel(valid_time=slice('2022-07-30 13:00:00','2022-07-31 12:00:00'))
tp_all=tp_all.to_dataframe().reset_index(level=['latitude', 'longitude','valid_time'])
tp_all = tp_all.groupby(["latitude","longitude"]).tp.sum().reset_index()

# temp,lsm 12UTC 
era5_vars=era5.sel(valid_time=('2022-07-31 12:00:00'))
era5_vars=era5_vars.to_dataframe().reset_index(level=['latitude', 'longitude'])
era5_vars=era5_vars[['latitude','longitude','t2m','lsm','valid_time']]

# previoud day dc & current day dc from historical data (verification)
dc = xr.open_dataset(grib_path+dc_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('time','verifying_time'),indexpath=''))
dc_t_1=dc.sel(time=slice('2022-07-30','2022-07-30'),latitude=slice(84,60))
dc_t=dc.sel(time=slice('2022-07-31','2022-07-31'),latitude=slice(84,60))
dc_t_1=dc_t_1.to_dataframe()
dc_t_1=dc_t_1.reset_index(level=['latitude', 'longitude','time'])
dc_t_1=dc_t_1[['latitude','longitude','time','drtcode']]
dc_t=dc_t.to_dataframe()
dc_t=dc_t.reset_index(level=['latitude', 'longitude','time'])
dc_t=dc_t[['latitude','longitude','time','drtcode']]  

'''
with open(path+'dc-check-test.csv','w') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    writer.writerow('lat,lon,lsm,t,p,sdeSUM,dc0,dc,dc_real')

cols = ['latitude', 'longitude', 'time','drtcode']
df = pd.DataFrame(columns=cols)
for index, row in dc_t_1.iterrows():
    lat=row['latitude']
    lon=row['longitude']
    dc0=row['drtcode']
    lsm=era5_vars.query('latitude =='+ str(lat)+' & longitude =='+ str(lon))['lsm'].item()
    t=era5_vars.query('latitude =='+ str(lat)+' & longitude =='+ str(lon))['t2m'].item() - 273.15    
    p=tp_all.query('latitude =='+ str(lat)+' & longitude =='+ str(lon))['tp'].item() * 1000
    dc_real=dc_t.query('latitude =='+ str(lat)+' & longitude =='+ str(lon))['drtcode'].item()
    sde3days=sde_mean.query('latitude =='+ str(lat)+' & longitude =='+ str(lon))['daily-mean-sde'].to_list()
    sdeSUM=sum(sde3days)    
    if pd.isna(dc0):
        if sdeSUM > 0.001: # if snow thickness above 0.001m , dc is nan (fix condition)
            dc=np.nan
        elif lsm<=0.01: # or if lsm water body, dc is nan (fix?)
            dc=np.nan 
        else: 
            dc=15# if previous is nan but no snow in 3 days, start with dc=15
    else:  
        if sdeSUM<0.001:
            dc=fidx.dc(t,p,mon,lat,lon,dc0)
        else: 
            dc=np.nan
    #writer.writerow([lat,lon,lsm,t,p,sdeSUM,dc0,dc,dc_real])
    print('lat,lon,lsm,t,p,sdeSUM,dc0,dc,dc_real')
    print(lat,lon,lsm,t,p,sdeSUM,dc0,dc,dc_real)
    df.loc[len(df)] = [lat, lon, t_0, dc]
    
df2array=df.to_xarray()
outFile=path+'result-DC-testi.nc'
ncfile=df2array.to_netcdf(outFile)
'''
executionTime=(time.time()-startTime)
print('time (min): %.2f'%(executionTime/60))

