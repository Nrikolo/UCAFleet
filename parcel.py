# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Riko
"""

import numpy as np

from mesa import Agent


class Parcel(Agent):
    '''
    A Parcel class.
    The agent has the following attributes:
        UUID (int) a unique identifier for this parcel  
        MASS (int) kg
        VOLUME (int) m^3 
        SOURCE (str) airport name
        DESTINATION (str) airport name
        TRANSPORTER (int) the uav uuid that has transported this parcel
        _LIFE_SPAN (int) the total time (number of steps) the parcel existed prior to reaching its desitnation
        age (int) the total time the parcel exists from inception to now
    
    '''
    def __init__(self, unique_id, model, source_name, destination_name, pdf_params = None):
        '''
        Create a parcel agent.
        Args:
            unique_id - Unique parcel identifyer
            model - the ABM model
            source_name - the airport this parcel is instantiated in 
            pdf_params - probability mass/density function type and parameters #TODO
        '''
        super().__init__(unique_id, model)
        self.type_ = 'parcel'
        self.SOURCE = source_name
        self.DESTINATION = destination_name
        #TODO: use random.choice(self.model.schedule.agents) 
        #would require implementing a custom scheduler with 2 types of agents
        #this would select a random agent (airport) from the list of available airports excluding the input 
        self.TRANSPORTER = None # UUID of transporting uav
        self.MASS = 2.5 * np.random.randn() + 10
        self.VOLUME = 2.1 * np.random.randn() + 1
        self.age = 0
        self._LIFESPAN = None 
        
    def parcel_mass():
        pass
        
    def parcel_volume():
        pass        
        
    def increment_age(self): 
        '''
        Increments the age of the parcel by a single step 
        '''
        self.age += 1 
    
    def delivered(self): 
        '''
        upon arrival to destination, parcel is assumed delivered, its "destroyed" conceptually
        by setting its _LIFE_SPAN to its current age. 
        '''
        self._LIFESPAN = self.age
        
    def get_lifespan(self):
        '''
        accesor function for parcel life span 
        '''
        return self._LIFESPAN
    
    def step(self):
        '''
        
        '''
        self.increment_age()
        
    