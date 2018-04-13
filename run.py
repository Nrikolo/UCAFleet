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
     'x' : [0., 450.],
     'y' : [0., 200.  ],
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
simlation_span = 10 
#Each step is one minute!!!


model = Fleet(airports,
              num_uav_per_airport,
              steps_per_hour = 60,
              width=500,
              height = 500)

#for i in range(simlation_span):
#    model.step()



#parcel_age = [parcel._LIFESPAN for a in model.schedule.agents]
#plt.hist(parcel_age)
#plt.show()
print ("UNIT TESTING OUTPUT")
mtl = model.get_airportObj('Montreal')
mtl.parcel_queues[0].generate_parcels(5)
mtl.parcel_queues[0].get_size()
mtl.parcel_queues[0].get_mass()
mtl.parcel_queues[0].get_shipment(50,200)


