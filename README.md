
# Large Unmanned Cargo Aircraft Delivery Fleet

## Summary 

Build upon the mesa package, this is an agent based model simulating a network/fleet 
of UAVs carrying packages from point A to B. Each of those points is an airport.
Those packages are randomly generated at each airport with random physical attributes
as well as a destination. 

UAVs are tasked with transporting those payloads from their present location to 
the destination. 

The aim is to maximize UAV utilization while minimizing package life span. 

## Characteristics 

* The UAV is based on a Dominator XP from Aeronautics. A modified Diamond DA 42 to an RPAS.
* The airport network is based on actual city distances in eastern Canada.  

## Assumptions

* There is no limit as to the number of UAV in a single airport
* The model doesn't support "hub and spoke" routing. Meaning, a package source 
and destination must be connected by a single flight segment. 
* Each airport is connected to all the other airports (Will be changed in the future) 
* No prioritization of queues for loading. Meaning, uavs attempt to load from 
the source airport queues based on which was instansiated first
* UAV fuel consumption is constant
* Airport refuelling rate is constant 

## Files

* ``run.py``: Launches a model.
* ``run_viz.py``: Launches the model visualization server
* ``input_data.py``: Defined the input data, i.e airports and their name, loci,
 parcel generation attributes and refuel rates.
* ``model.py``: Contains the agent class, and the overall model class.
* ``uav.py``: Contains the uav agent class
* ``airport.py``: Contains the airport agent class
* ``parcel.py``: Contains the parcel (package) class 
* ``parcelqueue.py``: Contains the parcel queue class 
* ``flight.py``: Defined a namedtuple used for uav flight logs 
* ``schedule.py``: Defines the schedule
* ``server.py``: Defines classes for visualizing the model in the browser via 
Mesa's modular server, and instantiates a visualization server.
* ``agent_portrayal.py``: Defined the agent type based visualization attributes
* ``auxfunctions.py``: Defined auxilliary functions 





