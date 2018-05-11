# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:23:36 2018

@author: Riko
"""
import pandas as pd
#Specify the names and locations of the airports
#d = {'Name': ['Toronto','Montreal','Ottawa', 'Quebec City'],
#     'x'   : [10.       , 410.     , 310. , 710.],
#     'y'   : [10.       , 410.     , 410. , 710.],
#     'pdf_params' : [1,1,1,1], 
#     'refuelling_rate':[10,10,10,10],
#     'num_uavs':[5,5,5,5]}

d = {'Name': ['Toronto','Montreal','Ottawa'],
     'x'   : [10.       , 510.     , 210.  ],
     'y'   : [10.       , 410.     , 410.  ],
     'pdf_params' : [1,1,1], 
     'refuelling_rate':[10,10,10],
     'num_uavs':[1,2,3]}

#Convert to dataframe
airports = pd.DataFrame(d)
del d
#Use 'Name' as index column
airports.set_index('Name',drop=True, inplace=True)

steps_per_hour = 60