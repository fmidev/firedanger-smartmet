import xarray as xr
import cfgrib, requests, csv
import pandas as pd
import numpy as np
import time, sys
import fireindices as fidx
from datetime import datetime,timedelta
startTime=time.time()
######################
### Calculate starting fire indexes from ECFWI to ERA5 
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

grib_path='/home/users/smartmet/data/grib/'
path='/home/users/smartmet/data/'

t=sys.argv[1]
mon=int(t[5])

dc0_file=sys.argv[2]
vars_t_file=sys.argv[3] 
vars_t_1_file=sys.argv[4] 
sde_t_file=sys.argv[5] 
sde_t_1_file=sys.argv[6] 
sde_t_2_file=sys.argv[7] 

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

day0date = datetime.strptime(t, '%Y%m%d').date()
day1date = str(day0date - timedelta(days=1))
day2date = str(day0date - timedelta(days=2))

day012 = datetime.strptime(t, '%Y%m%d') + timedelta(days=0,hours=12) # day0date 12:00:00
day113 = datetime.strptime(t, '%Y%m%d') - timedelta(days=0,hours=11) # day1date 13:00:00

# 24h precipitation accumulation (12:00:00UTC - 12:00:00UTC)
tp_all=era5.sel(valid_time=slice(day113,day012)) # day1date 13:00:00, # day0date 12:00:00
tp_all=tp_all.to_dataframe().reset_index(level=['latitude', 'longitude','valid_time'])
tp_all = tp_all.groupby(["latitude","longitude"]).tp.sum().reset_index()

# temp,lsm 12UTC 
era5_vars=era5.sel(valid_time=(day012)) # day0 12:00:00
era5_vars=era5_vars.to_dataframe().reset_index(level=['latitude', 'longitude'])
era5_vars=era5_vars[['latitude','longitude','t2m','lsm','valid_time']]

# previoud day dc & current day dc from historical data (verification)
dc = xr.open_dataset(grib_path+dc0_file, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('time','verifying_time'),indexpath=''))
dc_t_1=dc.sel(time=slice(day1date,day1date),latitude=slice(84,60))
dc_t=dc.sel(time=slice(day0date,day0date),latitude=slice(84,60))
dc_t_1=dc_t_1.to_dataframe()
dc_t_1=dc_t_1.reset_index(level=['latitude', 'longitude','time'])
dc_t_1=dc_t_1[['latitude','longitude','drtcode']]
dc_t_1.rename(columns = {'drtcode':'dc0'}, inplace = True)
dc_t=dc_t.to_dataframe()
dc_t=dc_t.reset_index(level=['latitude', 'longitude','time'])
dc_t=dc_t[['latitude','longitude','drtcode']]  
dc_t.rename(columns = {'drtcode':'dc_real'}, inplace = True)

dfs = [dc_t_1, dc_t, tp_all,era5_vars,sde_sum]
dfs = [df.set_index(['latitude','longitude']) for df in dfs]
dfs=dfs[0].join(dfs[1:])
dfs['tp']=dfs['tp']*1000 # m to mm
dfs['t2m']=dfs['t2m']-273.15 # K to celsius
dfs.rename(columns = {'valid_time':'time'}, inplace = True)

Lf=[-1.6,-1.6,-1.6,0.9,3.8,5.8,6.4,5.0,2.4,0.4,-1.6,-1.6] # day-length factor for 45deg, change to arctic

dfs['dc']=''
# dc0 nan, either dc_new nan or 15 starting value
dfs.loc[(pd.isna(dfs['dc0'])) & (dfs['sdesum']>0.001) | (pd.isna(dfs['dc0'])) & (dfs['lsm']<=0.01),'dc'] = np.nan
dfs.loc[(pd.isna(dfs['dc0'])) & (dfs['sdesum']<=0.001) & (dfs['lsm']>0.01),'dc'] = 15

# dc0 has value, either dc_new nan due to snow or dc_new calculated with function call
# dc0 is not nan but sde > 0
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']>0.001),'dc'] = np.nan
# dc0 is not nan and sde = 0: if t<-2.8: t=-2.8
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001) & (dfs['t2m']<=-2.8),'t2m']=-2.8
# dc0 is not nan and sde = 0: pev
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001),'pev']=0.36*(dfs['t2m']+2.8)+Lf[mon]
# dc0 is not nan and sde = 0 and pev < 0: pev = 0
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001) & (dfs['pev']<0),'pev'] = 0
# dc0 is not nan and sde = 0: dcr_t 
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001),'dcr_t']=400*np.log(800/(800*np.exp(-dfs['dc0']/400)+3.937*(0.83*dfs['tp']-1.27)))
# dc0 is not nan and sde = 0 and dcr_t <0 : dcr_T = 0
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001) & (dfs['dcr_t']<0.0),'dcr_t']=0.0
# dc0 is not nan and sde = 0 and tp>2.8: calculate dc with dcr_ti and pev
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001) & (dfs['tp']>2.8),'dc']=dfs['dcr_t']+0.5*dfs['pev']
## dc0 is not nan and sde = 0 and tp<=2.8: calculate dc with dc0 and pev
dfs.loc[(pd.isna(dfs['dc0'])==False) & (dfs['sdesum']<0.001) & (dfs['tp']<=2.8),'dc']=dfs['dc0']+0.5*dfs['pev']

dfs['time'] = pd.DatetimeIndex(dfs['time'].values)
dfs=dfs.reset_index(level=['latitude', 'longitude'])
dfs=dfs.set_index(['time','latitude', 'longitude'])
apu=dfs[['dc0','dc_real','dc']].dropna()
apu.to_csv('testi.csv')
dfs2csv=dfs[['dc']]
dfs2csv.loc[(pd.isna(dfs['dc'])),'dc'] = -99999 # change nan to -99999
print(dfs2csv)


df2array=dfs2csv.to_xarray()
#print(df2array)
dayOut = str(datetime.strptime(t, '%Y%m%d').date() + timedelta(days=1)).replace('-','')
outFile=path+'dc-out-'+dayOut+'.nc'
ncfile=df2array.to_netcdf(outFile)

executionTime=(time.time()-startTime)
print('time (min): %.2f'%(executionTime/60))

