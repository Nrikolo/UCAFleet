# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:47:22 2018

@author: Riko
"""

import time
from model import Fleet
from input_data import airports, steps_per_hour
from graph_function import graph_function
import logging

#run.py 
#is a Python script that will run the model when invoked as python run.py.
#Similar to a main. 

#Specify the amount of time in hours for the simulation to run
simulation_time = 5 
simlation_steps = simulation_time * steps_per_hour

logging.basicConfig(filename='FleetLog.log',
                    format='%(asctime)s : %(levelname) : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


start_time = time.time()  # Execution time counter start
#with auxfunctions.suppress_stdout():
model = Fleet(airports,
                  steps_per_hour,
                  width=2000,
                  height = 2000)
for i in range(simlation_steps):
    model.step()

logging.shutdown()

end_time = time.time()  # Execution time counter start
execution_time = end_time - start_time

graph_function(model, simulation_time, execution_time)