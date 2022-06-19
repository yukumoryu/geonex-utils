#!/usr/bin/env python
# coding: utf-8

# # pre

# In[ ]:


import numpy as np
import pandas as pd
import glob
from Utilities import *
utils = init()
from tqdm import tqdm


# In[ ]:


# # Generate the sha256 of this row of data
# import hashlib
# def cal_row_sha256(_DataFrame_,x):
#     _tmp_ = hashlib.sha256(str( _DataFrame_[x_:x_+1] ).encode()).hexdigest()
#     return _tmp_


# In[ ]:


### The basis for the entire handling of dependencies
site_info_ = pd.read_csv('./res.csv',header=1)


# In[ ]:


### Generate some time series to spare
start_date='2018-01-01'
start_time='00:00:00'
end_date='2020-12-31'
end_time='23:55:00'
interval='15min'
timestamp_5min = pd.date_range(start = start_date+' '+start_time,end=end_date+' '+end_time,freq='5min')
timestamp_15min = timestamp_range(start_date,start_time,end_date,end_time,interval)
timestamp_30min = pd.date_range(start = start_date+' '+start_time,end=end_date+' '+end_time,freq='30min')
timestamp_1h = pd.date_range(start = start_date+' '+start_time,end=end_date+' '+end_time,freq='1h')
timestamp_3h = pd.date_range(start = start_date+' '+start_time,end=end_date+' '+end_time,freq='3h')
timestamp_2018_30min = pd.date_range(start = '2018-01-01'+' '+start_time,end='2018-12-31'+' '+end_time,freq='30min')
timestamp_2019_30min = pd.date_range(start = '2019-01-01'+' '+start_time,end='2019-12-31'+' '+end_time,freq='30min')
timestamp_2020_30min = pd.date_range(start = '2020-01-01'+' '+start_time,end='2020-12-31'+' '+end_time,freq='30min')
one_year_offset_30min = timestamp_2018_30min.shape[0]


# In[ ]:


abi05_head = ['Solar_Zenith', 'Solar_Azimuth', 'BAND01', 'BAND02',
       'BAND03', 'BAND04', 'BAND05', 'BAND06', 'BAND07', 'BAND08', 'BAND09',
       'BAND10', 'BAND11', 'BAND12', 'BAND13', 'BAND14', 'BAND15', 'BAND16',
       'Lat', 'Lon', 'timestamp']


# # Data concat & resample

# In[ ]:


for i in tqdm(range(len(site_info_))):
    # set file path (Example output data)
    tt_ = pd.read_csv((f'/home/yakumohitomi/T/abi_file_data/goes_16_h{site_info_._HID_[i]:0>2d}_v{site_info_._VID_[i]:0>2d}_{site_info_.Site_Id[i]}_{timestamp_15min.start_date}_{timestamp_15min.end_date}.csv') )
    tt_['timestamp']=timestamp_5min
    tt_ = tt_.drop(columns='Unnamed: 0')
    # Resample to the time frequency you need （ example 30min )
    ttrm = tt_.resample('30min',on='timestamp').mean()
    
    ### The following is splicing a flux data of the same time resolution into a table ###
    # You can add the fluxnet data you need
    sd_ = pd.read_csv(glob.glob(f'/data/ssd1/FLX_{site_info_.Site_Id[i]}_FLUXNET2015_FULLSET_HH_{site_info_.start_year[i]}-{site_info_.end_year[i]}_beta-3.csv')[0]) 
    # Select the name of the header of the data you need
    sd_gpp_VUT_50 = sd_.filter(['TIMESTAMP_START','GPP_DT_VUT_50'])[int(np.argwhere(np.array(sd_.TIMESTAMP_START) == 201801010000)):]
    sd_gpp_VUT_50['TIMESTAMP_START']=pd.date_range(start = '2018-01-01'+' '+start_time,end=f'{site_info_.end_year[i]}-12-31'+' '+end_time,freq='30min')
    sd_gpp_VUT_50 = sd_gpp_VUT_50.set_index('TIMESTAMP_START')
    tmp_ = pd.concat( [ttrm,sd_gpp_VUT_50],axis=1)
    
    ### set output path
    tmp_.to_csv(f'/home/yakumohitomi/T/abi_file_data/30min/goes_16_h{site_info_._HID_[i]:0>2d}_v{site_info_._VID_[i]:0>2d}_{site_info_.Site_Id[i]}_{timestamp_15min.start_date}_{timestamp_15min.end_date}_30min.csv')


# In[ ]:


# ttrm.shape[0]
# index_ = []
# for x_ in tqdm( range(ttrm.shape[0]) ):
#     index_.append( cal_row_sha256(ttrm,x_) )

