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
     'x' : [0., 400.],
     'y' : [0., 400.  ],
     'pdf_params' : [1,1], 
     'refuelling_rate':[30,30],
     'num_uavs':[1,1]}
#Convert to dataframe
airports = pd.DataFrame(d)
del d
#Use 'Name' as index column
airports.set_index('Name',drop=True, inplace=True)

#Specify the amount of time in hours for the simulation to run
simulation_time = 24 

steps_per_hour = 60  # Each step is one minute!!!
simlation_steps = simulation_time * steps_per_hour

model = Fleet(airports,
              steps_per_hour,
              width=500,
              height = 500)

for i in range(simlation_steps):
    model.step()



print ("UNIT TESTING OUTPUT---------------------------------------")
#model.step()
mtl = model.get_airport_obj('Montreal')
tor = model.get_airport_obj('Toronto')
from uav import Uav
uavs = model.schedule.agents_by_type[Uav]

print ("GRAPHS---------------------------------------")
import matplotlib.pyplot as plt
from parcel import Parcel
parcel_age = [p.age / steps_per_hour for p in model.schedule.agents_by_type[Parcel]]
plt.hist(parcel_age)
plt.show()

from uav import Uav
TFH = [u._tfh for u in model.schedule.agents_by_type[Uav]]
utilization = [x / simulation_time*100 for x in TFH]
plt.hist(utilization)
plt.show()


