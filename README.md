"""
Created on Fri Mar 16 15:45:27 2018

@author: Riko
"""

#!Work in progress!

#Large Unmanned Cargo Aircraft Delivery Fleet

##Summary 

Build upon the mesa package, this is an agent based model simulating a network/fleet 
of UAVs carrying payloads from point A to B. Those payload are randomly generated 
at each airport with random physical attributes as well as a destination. 

UAVs are tasked with transporting those payloads from their present location to 
the destination. 

## Files

* ``run.py``: Launches a model visualization server.
* ``model.py``: Contains the agent class, and the overall model class.
* ``uav.py``: Contains the uav agent class
* ``airport.py``: Contains the airport agent class
* ``package.py``: Contains the package class (non agent)
* ``server.py``: Defines classes for visualizing the model in the browser via Mesa's modular server, and instantiates a visualization server.
