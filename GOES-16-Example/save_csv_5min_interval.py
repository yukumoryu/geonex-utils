from Utilities import *
utils = init()
import glob,os,datetime,time
from pyhdf.SD import SD, SDC
import numpy as np
import pandas as pd
import scipy

site_info_ = pd.read_csv('res.csv',header=1) 
### The control file will cycle according to this table

times_5min_ = timestamp_range(start_date='2018-01-01',
                 start_time='00:00:00',
                 end_date='2020-12-31',
                 end_time='23:55:00',
                 interval='5min') 
### Set start and end time and interval
                 
    
for i in range(len(site_info_)):
    point_num = ReadWithTime( times_5min_,
                             f'/data/hdd/DL/geonex/h{site_info_._HID_[i]:0>2d}v{site_info_._VID_[i]:0>2d}/',
                             site_info_._HID_[i],site_info_._VID_[i],site_info_.Lat[i],site_info_.Long[i],
                             proc=utils)
    dfs = DataFillter(pd.DataFrame(point_num))  
    ### Set your own Geonex path
    dfs.to_csv(f'./abi_file_data/goes_16_h{site_info_._HID_[i]:0>2d}_v{site_info_._VID_[i]:0>2d}_{site_info_.Site_Id[i]}_{times_5min_.start_date}_{times_5min_.end_date}.csv')
### set output path
