# GEONEX-utils 
If it helps you please give me a star or feedback

Features :
* Generate download list as needed
* Apply data corrections
* Single point extraction tool
* Resampling from time series ( can add the fluxnet data you need )
* ......

Dependencies:
- python 3
- numpy
- pandas
- tqdm
- pyhdf
- glob
- regex

File tree of example processing cases：

```
/data/hdd/DL/geonex/
├── h09v01
│   ├── GO16_ABI05_20180101_0000_GLBG_h09v11_02.hdf
│   ├── .........
├── h11v04
│   ├── .........
├── .............
```
About geonex data download :
* Because geonex data portal seems to be just a front end, the actual back end does not need to be requested from the page, so we can directly generate a download list and download it with wget
