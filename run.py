# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:47:22 2018

@author: Riko
"""

import pandas as pd
import numpy as np

from model import Fleet


    
#run.py 
#is a Python script that will run the model when invoked as python run.py.
#Similar to a main. 



#Specify the names and locations of the airports
d = {'Name':['A','B'],
     'x' : [0., 200.],
     'y' : [0., 0.  ],
     'pdf_params' : [1,1], 
     'refuelingRate':[30,30]}
#Convert to dataframe
airports = pd.DataFrame(d)
#Use 'Name' as index column
airports.set_index('Name',drop=True, inplace=True)
#print (airports)

#Specify the allocations of UAVs per airport 

#We shall specify the total number of UAVs
#Those are presently evenly and randomly distributed within airports
num_uavs = 1 


#Specify the amount of time (number of steps) the simulation is to run
simlation_span = 10 #two hours
#Each step is one minute!!!


model = Fleet(airports,num_uavs, steps_per_hour = 60, width=500, height = 500)

#for i in range(simlation_span):
#    model.step()
