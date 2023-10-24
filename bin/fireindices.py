import pandas 
import numpy as np

def dc(t,p,mon,lat,lon,dc0):
    ''' Drought code (Canadian)
    t: noon temperature [C]
    p: 24h precipitation accumulation [mm]
    mon: month of year [1-12]
    dc0: previous day value for drought code
    lat (lon): for Lf later add
    '''
    Lf=[-1.6,-1.6,-1.6,0.9,3.8,5.8,6.4,5.0,2.4,0.4,-1.6,-1.6] # day-length factor for lat 45deg
    if t < -2.8:
        t = -2.8
    pev=0.36*(t+2.8)+Lf[int(mon)] # potential evapotranspiration
    if pev < 0:
        pev = 0
    if p > 2.8:
        p_d=0.83*p-1.27 # effective rainfall
        q_t_1=800*np.exp(-dc0/400) # moisture equivalent of previous day DC
        qr_t=q_t_1+3.937*p_d # moisture equivalent after rain
        dcr_t=400*np.log(800/qr_t) # dc after rain
        if dcr_t < 0:
            dcr_t = 0
        dc_t=dcr_t+0.5*pev
    else: 
        dc_t=dc0+0.5*pev

    return dc_t