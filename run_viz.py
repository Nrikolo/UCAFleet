# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:47:22 2018

@author: Riko
"""


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

# TODO: visualization should be only done for airports and uavs agent types , 
# would probably require a null function for portrayal of parcels

#run.py 
from server import server
server.port = 8521 # The default   
server.launch()


