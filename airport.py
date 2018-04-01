# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:49:52 2018

@author: Riko
"""

import numpy as np
#TODO: this import should be placed in the model? 
from queue import Queue

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
        super().__init__(unique_id, model)
        self.name = name
        self.pos = np.array(pos)
        self.REFUELING_RATE = refueling_rate
        self.PDF = pdf
        self.uav_queue = Queue()
        # Need to loop through all airports (as possible) destinations
        
        self.parcel_queues = list()   
        
        
    def load_uav(self,UAV):
        '''
        provide a list (or queue) of packages to be transported by calling uav
        
        If there are more than MIN_PAYLOAD packages for one destination 
        function will load (for now return) a list of packages
        '''
        
    def generate_parcels(): 
        '''
        generates parcels in the airport based on probability density function 
        '''
        self.parcel_queues[]
        pass
    
    def step(self):
        '''
        A step in the airports timeline. Refuling UAVs, Loading UAVs and Generating packages
        '''
        
        # UAVs are self refueling if their state allows it 
        
        # Generate packages based on probability density function parameters 
        self.generate_parcels()        
        # Loop through the UAV Queue (FIFO) 
            #Try and load it 
            self.load_uav(first_in_line)  # Loop though parcel's queues 
            # If enough package exist for a destination, 
                # load on that UAV
        
         