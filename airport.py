# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:49:52 2018

@author: Riko
"""

import numpy as np
#TODO: this import should be placed in the model? 
#from queue import Queue

from mesa import Agent


class Airport(Agent):
    '''
    A Airport agent with the following attributes:
        NAME (string)
        Package Queues {one for each of the other airports} #those within range???
        Package PDF (probability density function)
        UAV Queue (FIFO queue) of UAV agents in that airport
        POSITION (x,y) in km
        REFUELING_SPEED in Liters/step 
  

    '''
    def __init__(self, unique_id, model, name, pos,refuelingSpeed , pdf):
        '''
        Create a airport agent.
        Args:
            speed: Distance to move per step.

        '''
        super().__init__(unique_id, model)
        self.NAME = name
        self.pos = np.array(pos)
        self.REFUELING_SPEED = refuelingSpeed
        self.PDF = pdf
        
    def load_uav(self,UAV):
        '''
        provide a list (or queue) of packages to be transported by calling uav
        
        Loops through source queues and selects a set of packages to load 
        If there are more than MIN_PAYLOAD packages for one destination 
        function will load (for now return) a list of packages
        

        '''
        