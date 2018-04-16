# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:47:22 2018

@author: Riko
"""

import time
import auxfunctions
from model import Fleet
from input_data import airports, steps_per_hour

# TODO: visualization of the fleet such that each airport is a node with  
# a list of queues next to it. Each queue indicates the total number of parcels
# in it, oldest and average age

# TODO: include a flight log for each uav. Flight log would hold a list of 
# flights conducted by uav, each with 
# {source, destination, distance, duration, payload, fuel}

# TODO: Visualization of parcels state. A pie chart where each sector indicates 
# either {awaiting, onroute, delivered} 
    
# TODO: Visualization of parcels state. A line chart where each line indicates 
# the total numder of parcels {awaiting, onroute} as s function of time
#--> should indicate steady-state if reached

# TODO: Payload utilization (how much of the payload on the uav is being used)
# Compute average, min, max, stdev payload utilization (%) for all flights


# TODO: In preparatio for batch running, compute the following metrics to qualify a sim:
# Percent parcels delivered, 
#{min, max, average, stdev} age of parcels, 
#{min, max, average, stdev} % utilization of uavs




#run.py 
#is a Python script that will run the model when invoked as python run.py.
#Similar to a main. 

#Specify the amount of time in hours for the simulation to run
simulation_time = 10 

simlation_steps = simulation_time * steps_per_hour


#from server import server
#server.port = 8521 # The default
#server.launch()

start_time = time.time()  # Execution time counter start

#with auxfunctions.suppress_stdout():
model = Fleet(airports,
                  steps_per_hour,
                  width=2000,
                  height = 2000)

for i in range(simlation_steps):
    model.step()


end_time = time.time()  # Execution time counter start
execution_time = end_time - start_time

print ("UNIT TESTING OUTPUT---------------------------------------")
#model.step()
#mtl = model.get_airport_obj('Montreal')
#tor = model.get_airport_obj('Toronto')
#from uav import Uav
#uavs = model.schedule.agents_by_type[Uav]


print ("GRAPHS---------------------------------------")
import matplotlib.pyplot as plt
from parcel import Parcel
parcel_age = [p.age / steps_per_hour for p in model.schedule.agents_by_type[Parcel]]
plt.hist(parcel_age)
plt.show()
print("This simulation was running for {} hours and ran for {:.2f}sec \n" \
      "During which {} parcels were generated, {} were " \
      "delivered, {:.2f} % ".format(model.schedule.steps / model.get_steps_per_hour(),
                                    execution_time,
                                    len(parcel_age),
                                    len(model.parcel_aggregator),
                                    100*len(model.parcel_aggregator) / len(parcel_age)))

from uav import Uav
TFH = [u._tfh for u in model.schedule.agents_by_type[Uav]]
utilization = [x / simulation_time*100 for x in TFH]
plt.hist(utilization)
plt.show()


