# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:47:22 2018

@author: Riko
"""

import pandas as pd

from model import Fleet



    
#run.py 
#is a Python script that will run the model when invoked as python run.py.
#Similar to a main. 



#Specify the names and locations of the airports
d = {'Name':['Toronto','Montreal'],
     'x' : [0., 100.],
     'y' : [0., 0.  ],
     'pdf_params' : [1,1], 
     'refueling_rate':[30,30]}
#Convert to dataframe
airports = pd.DataFrame(d)
del d
#Use 'Name' as index column
airports.set_index('Name',drop=True, inplace=True)
#print (airports)

#Specify the allocations of UAVs per airport 


#We shall specify the total number of UAVs
total_num_uavs = 2
num_uav_per_airport = int( total_num_uavs / len(airports))


#Specify the amount of time (number of steps) the simulation is to run
simlation_span = 1000 
#Each step is one minute!!!


model = Fleet(airports,
              num_uav_per_airport,
              steps_per_hour = 60,
              width=500,
              height = 500)

for i in range(simlation_span):
    model.step()



#parcel_age = [parcel._LIFESPAN for a in model.schedule.agents]
#plt.hist(parcel_age)
#plt.show()
print ("UNIT TESTING OUTPUT---------------------------------------")
#model.step()
mtl = model.get_airportObj('Montreal')
tor = model.get_airportObj('Toronto')
from uav import Uav
uavs = model.schedule.agents_by_type[Uav]
#
#
#mtl.parcel_queues[0].generate_parcels(5)
#mtl.parcel_queues[0].get_size()
#mtl.parcel_queues[0].get_mass()
#mtl.parcel_queues[0].get_shipment(50,200)
#
#uavObj = mtl.uav_queue[0]
#uavObj.is_loaded()
#print ("------------------")
#mtl.step()
#print ("------------------")
#uavObj.step()
#uavObj.step()
#uavObj.step()
#print ("------------------")
#tor.uav_queue

import matplotlib.pyplot as plt
from parcel import Parcel
parcel_age = [p.age for p in model.schedule.agents_by_type[Parcel]]
plt.hist(parcel_age)
plt.show()
