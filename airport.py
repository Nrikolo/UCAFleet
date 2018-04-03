# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:49:52 2018

@author: Riko
"""

import numpy as np
#TODO: this import should be placed in the model? 
from queue import Queue
from collections import deque, defaultdict
from parcelqueue import ParcelQueue
from mesa import Agent


class Airport(Agent):
    '''
    A Airport agent with the following attributes:
        NAME (string)
        Package Queues {one for each of the other airports} #those within range???
        Package PDF (probability density function)
        UAV Queue (FIFO queue) of UAV agents in that airport
        pos (x,y) in km
        REFUELING_RATE in Liters/step 
    '''
    
    name_index = defaultdict(list)
    def __init__(self, unique_id, model, name, pos, refueling_rate, pdf):
        '''
        Create a airport agent.
        Args:
            unique_id: UUID
            model: 
            name: 
            pos:
            refuling_rate:
            pdf:

        '''
        print("Creating an airport instance with id {} in {}".format(unique_id,name))
        super().__init__(unique_id, model)
        self.type_ = 'airport'
        self.name = name
        self.pos = np.array(pos)
        self.REFUELING_RATE = refueling_rate
        self.PDF = pdf
#        self.uav_queue = Queue()  # An empty queue for UAVs 
        self.uav_queue = deque()  # An empty queue for UAVs 
        self.parcel_queues = list()   
        # Create a parcel queue for each of the OTHER airports in the model 
        # Assumes all airports are within range and a single flight is required to deliver a parcel
        for index,row in self.model._airports.iterrows():
            if index == self.name:  # Airport from the list is the same as being constructed 
                continue 
            self.parcel_queues.append(ParcelQueue(self.model,self.name, index))  # Create a parcel queue
        
        Airport.name_index[self.name].append(self)

        
    @classmethod
    def find_by_name(cls,name): 
        return Airport.name_index[name]


    def store_uav(self,uavObj): 
        '''
        recieve a uav object and store it in the airport's FIFO queue 
        '''
        self.uav_queue.append(uavObj)
        
        
        
    def _load_uav(self,uavObj):
        '''
        #TODO: update dox for actual implementation
        provide a list (or queue) of packages to be transported by calling uav
        
        If there are more than MIN_PAYLOAD packages for one destination 
        function will load (for now return) a list of packages
        '''
        
        for q in self.parcel_queues: 
            #iterate throught the queue of parcels for a specific destination
            shipment, shipment_mass = q.get_shipment(self, uavObj.MAX_PAYLOAD)
            uavObj.load(shipment, q.DESTINATION)
        #return true if loaded 

        
    def _sort_parcel_queues(self, priority=None):
        '''
        sorts the airport's parcel queues based on criteria 
        '''
        #TODO: decide on the order of priority to loop though the parcel queues 
        # in the airport. it would make sense that self.parcel_queues is sorted based on the criteria
        # Consider implementing one or all
        # --The q with the most packages (Priority = amount)
        # --The q with the oldest package (Priority = oldest)
        # --The q with the highest average age (Priority = oldest_avg)
        pass
    
    def _generate_parcels(self): 
        '''
        generates parcels in the airport based on probability density function 
        '''
        #TODO: use pdf_parameters 
        
        # Iterate through all parcel queue objects and generate parcels
        for q in self.parcel_queues:
            q.generate_parcels()
    
    def step(self):
        '''
        A step in the airports timeline. Refuling UAVs, Loading UAVs and Generating packages
        '''
        
        # UAVs are self refueling if their state allows it 
        
        self._generate_parcels() 
        self._sort_parcel_queues()
        
        for uavObj in self.uav_queue: # Loop through the UAV Queue (FIFO) 
            if uavObj.is_IDLE(): #verify it is idle and ready to load
                print ("Attempting to load {}".format(uavObj.uniqe_id))
                #Try and load it 
                self._load_uav(uavObj)  # Loop though parcel's queues 
            else: 
                continue 
            # If enough package exist for a destination, 
                # load on that UAV
        
         