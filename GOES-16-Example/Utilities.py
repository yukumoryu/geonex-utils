#!/bin/env python3
import math
import re as regex
import numpy as np
import pandas as pd
from tqdm import tqdm
from pyhdf.SD import SD, SDC

class init():
    def __init__(self):
        ############ offset ######################
        self.lat_0 = 60
        self.lon_0 = -180
        self.res2km   = np.linspace(0,6,301)[1]
        self.res1km   = np.linspace(0,6,601)[1]
        self.res500m = np.linspace(0,6,1201)[1]
        self.res2km_offset   = self.res2km/2 # center offset
        self.res1km_offset   = self.res1km/2 # _
        self.res500m_offset = self.res500m/2 # _
        ####################################################################
        ###################### for  center longitude #######################
    def hid_vid_to_lat_lon_center(self,hid,vid,res):
        if res == '2km':
            start_lat   = (20-int(vid))*6-60-self.res2km_offset
            start_lon  = int(hid)*6-180+self.res2km_offset        
            end_lat    = (20-int(vid))*6-60-6+self.res2km_offset
            end_lon   = int(hid)*6-180+6-self.res2km_offset
            return start_lat,end_lat,start_lon,end_lon
        elif res == '1km':
            start_lat   = (20-int(vid))*6-60-self.res1km_offset
            start_lon  = int(hid)*6-180+self.res1km_offset       
            end_lat    = (20-int(vid))*6-60-6+self.res1km_offset
            end_lon   = int(hid)*6-180+6-self.res1km_offset
            return start_lat,end_lat,start_lon,end_lon
        elif res == '500m':
            start_lat   = (20-int(vid))*6-60-self.res500m_offset
            start_lon  = int(hid)*6-180+self.res500m_offset
            end_lat    = (20-int(vid))*6-60-6+self.res500m_offset
            end_lon   = int(hid)*6-180+6-self.res500m_offset
            return start_lat,end_lat,start_lon,end_lon
        else:
            return print('###  hid-vid exchange error ###')
    ###########################################################################################
    #################  for upper-left corner & lower-right corner  ############################
    def hid_vid_lat_lon_exchange(self,hid,vid,res):
        start_lat   = (20-int(vid))*6-60
        start_lon  = int(hid)*6-180
        if res == '2km':
            end_lat    = (20-int(vid))*6-60-6
            end_lon   = int(hid)*6-180+6
            return start_lat,end_lat,start_lon,end_lon
        elif res == '1km':
            end_lat    = (20-int(vid))*6-60-6
            end_lon   = int(hid)*6-180+6
            return start_lat,end_lat,start_lon,end_lon
        elif res == '500m':
            end_lat    = (20-int(vid))*6-60-6
            end_lon   = int(hid)*6-180+6
            return start_lat,end_lat,start_lon,end_lon
        else:
            return print('###  hid-vid exchange error ###')
    ##################################################################    
    def make_lon_lat_corner_table(self,start,end,res):
        if res == '2km':
            return np.linspace(start,end,300+1)
        elif res == '1km':
            return np.linspace(start,end,600+1)
        elif res == '500m':
            return np.linspace(start,end,1200+1)
        else:
            return print('###  res error ###')
    ##################################################################
    ##################################################################
    def make_lon_lat_table(self,start,end,res):
        if res == '2km':
            return np.linspace(start,end,300)
        elif res == '1km':
            return np.linspace(start,end,600)
        elif res == '500m':
            return np.linspace(start,end,1200)
        else:
            return print('###  res error ###')
    ##################################################################
    ##################################################################
    def find_nearest(self,array,value):
        array = sorted(array)
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return array[idx-1]
        else:
            return array[idx]
    ##################################################################
    ##################################################################
    def get_point_number(self,hid,vid,res,find_lat,find_lon,array):
        start_lat, end_lat ,start_lon ,end_lon = self.hid_vid_to_lat_lon_center(hid,vid,res)
    #     print(start_lat,end_lat,start_lon,end_lon)
        tmp_lon_table = self.make_lon_lat_table(start_lon,end_lon,res)
    #     print(tmp_lon_table)
        tmp_lat_table = self.make_lon_lat_table(start_lat,end_lat,res)
    #     print(tmp_lat_table)
        lon_point = np.where(tmp_lon_table==self.find_nearest(tmp_lon_table,find_lon))
        lat_point = np.where(tmp_lat_table==self.find_nearest(tmp_lat_table,find_lat))  
    #     print(lon_point,lat_point)
    #     print(tmp_lon_table[lon_point])
    #     print(tmp_lat_table[lat_point])
        return array[lon_point,lat_point]
    ###################################################################################################
    def lat_lon_to_hid_vid(self,lat_,lon_):
        lat_ = np.array(lat_)
        lon_ = np.array(lon_)
        if (60>=lat_>=-60 and 180>=lon_>=-180):
            vid = int( np.array( np.where((np.sort(np.append( np.linspace(60,-60,20+1),lat_))[::-1])==lat_)   )-1 ) # LAT FIND VID 
            hid = int( np.array( np.where((np.sort(np.append( np.linspace(180,-180,60+1),lon_)))==lon_) )-1 ) # LON FIND HID 
            return hid,vid
        else:
            print('###  lat_lon_to_hid_vid error ###')
            return np.nan,np.nan

class File:
    def __init__(self, hid:int, vid:int, Lat:int, Lon:int, Date:str, Time:str, Satellite_Sensor_Code='GO16', ProductID='ABI05', version=2, path="./",proc=False):
        self.name = f"{Satellite_Sensor_Code}_{ProductID}_{Date}_{Time}_GLBG_h{hid:0>2d}v{vid:0>2d}_{version:0>2d}.hdf"
        self.path = path
        if self.path.split('.')[-1] != 'hdf':
            self.path = path+self.name
        self.Satellite_Sensor_Code = Satellite_Sensor_Code
        self.ProductID = ProductID
        self.Date = Date
        self.Time = Time
        self.hid = hid
        self.vid = vid
        self.point_number = {}
        self.dim = {}
        self.real_data = {}
        self.version = version
        self.Lat = Lon
        self.Lon = Lat
        self.sd = SD(self.path,SDC.READ)
        self.bands = list(self.sd.datasets().keys())
        for band in self.bands:
            self.dim[band] = regex.findall(r'.+:([0-9]{1,3}[k]{0,1}m)',str(self.sd.select(band).dimensions()))[0]
            obj = self.sd.select(band)
            self.point_number[band] = proc.get_point_number(hid=f'{self.hid:0>2d}',vid=f'{self.vid:0>2d}',
                                                       res=self.dim[band],find_lat=self.Lat,find_lon=self.Lon,array=obj.get())[0][0]
            data = (np.array([self.point_number[band]]) - obj.Offset_Constant)*obj.Scale_Factor
            nan_value = (obj._FillValue - obj.Offset_Constant)*obj.Scale_Factor
            data[data == nan_value]= np.nan
            nan_value = (32768-obj.Offset_Constant)*obj.Scale_Factor
            data[data == nan_value ]= np.nan
            self.real_data[band] = np.flip(data)[0]
            obj.endaccess()
        self.sd.end()
        
    def get_bands(self):
        return self.bands
    
    def get_position(self):
        return {"Lon":self.Lon,"Lat":self.Lat}
    
    def get_dim(self):
        return self.dim

    def get_info(self):
        return {"name":self.name,
                "path":self.path,
                "Satellite_Sensor_Code":self.Satellite_Sensor_Code,
                "ProductID":self.ProductID,
                "Date":self.Date,
                "Time":self.Time,
                "hid":self.hid,
                "vid":self.vid,
                "Lat":self.Lat,
                "Lon":self.Lon,
                "bands":self.bands,
                "version":self.version}

    def get_point_num_df(self):
        value = dict(self.point_number.items())
        value['Lat']=self.Lat
        value['Lon'] = self.Lon
        value['timestamp'] = self.Date+self.Time
        return value
    
    def get_real_data_dict(self):
        value = dict(self.real_data.items())
        value['Lat']=self.Lat
        value['Lon'] = self.Lon
        value['timestamp'] = self.Date+self.Time
        return value
        

def FlieInfo_parser(Filename,Lat,Lon):
    filename = Filename.split('/')[-1]
    Satellite_Sensor_Code, ProductID, Date, Time, hid, vid, version = regex.findall(
        r'([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([0-9]{8})_([0-9]{4})_GLBG_h([0-9]{2})v([0-9]{2})_([0-9]+)\.hdf',filename)[0]
    file = File(int(hid), int(vid), int(Lat), int(Lon), Date, Time, Satellite_Sensor_Code, ProductID, int(version), path=Filename)
    return file

def DataFillter(df):
    data_columns = ["BAND{:0>2d}".format(x) for x in range(1,7)]
    for column in data_columns:
        nptemp = df[column].to_numpy()
        df[column] = np.where( nptemp < 0,np.nan, nptemp)
        df[column] = np.where( nptemp > 1,1, nptemp)
    data_columns = ["BAND{:0>2d}".format(x) for x in range(7,17)]
    for column in data_columns:
        nptemp = df[column].to_numpy()
        df[column] = np.where( nptemp < 10,np.nan, nptemp)
    return df

def ReadWithTime(times,path,hid,vid,Lat,Lon,proc):
    point_num=[]
    for t in tqdm(times.time_range):
        try:
            file = File(hid,vid,Lat,Lon,Date=t[0],Time=t[1],path=path,proc=proc)
            point_num.append(file.get_real_data_dict())    
        except:
            print("IO Error,{SSC}_{PID}_{D}_{T}_GLBG_h{H:0>2d}v{V:0>2d}_{version:0>2d}.hdf".format(SSC='GO16',PID='ABI05',D=t[0],H=hid,V=vid,version=2,T=t[1]))
            point_num.append(dict(point_num[-1].items()))
            for key in point_num[-1].keys():
                if key not in ['Lat','Lon','timestamp']:
                    point_num[-1][key] = np.nan
            point_num[-1]['timestamp'] = str(t[0]+t[1])
    return point_num

class timestamp_range:
    def __init__(self,start_date,start_time,end_date,end_time,interval='15min'):
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.interval = interval
        self.date_range = pd.date_range(start = self.start_date+' '+self.start_time,end=self.end_date+' '+self.end_time,freq=self.interval)
        self.time_range = [x.split() for x in self.date_range.strftime('%Y%m%d %H%M').values]
        #self.time_range = [x.split() for x in self.date_range.strftime('%Y%m%d %H%M %j %Y').values]
        self.doy = self.date_range.strftime('%j').values
