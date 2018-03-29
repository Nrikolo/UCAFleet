# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Riko
"""

import numpy as np


class Package():
    '''
    A Package class.
    The agent has the following attributes:
        UUID (int) a unique identifier for this package  
        WEIGHT (int) kg
        VOLUME (int) m^3 
        SOURCE (str) airport name
        DESTINATION (str) airport name
        TRANSPORTER (int) the uav uuid that has transported this package
        _LIFE_SPAN (int) the total time (number of steps) the package existed prior to reaching its desitnation
        age (int) the total time the package exists from inception to now
    
    '''
    def __init__(self, unique_id, model, source_name, pdf_params):
        '''
        Create a package agent.
        Args:
            unique_id - Unique package identifyer
            model - the ABM model
            source_name - the airport this package is instantiated in 
            pdf_params - probability mass/density function type and parameters #TODO
        '''
        #super().__init__(unique_id, model)
        self.UUID = unique_id
        self.SOURCE = source_name
        self.DESTINATION = model.getRandomDestinationAirport(self.SOURCE)
        #TODO: use random.choice(self.model.schedule.agents) 
        #would require implementing a custom scheduler with 2 types of agents
        #this would select a random agent (airport) from the list of available airports excluding the input 
        self.TRANSPORTER = None 
        
        self.WEIGHT = 2.5 * np.random.randn() + 10
        self.VOLUME = 2.1 * np.random.randn() + 1
        self.age = 0
        self._LIFE_SPAN = None 
        
    def increment_age(self): 
        '''
        Increments the age of the package by a single step 
        '''
        self.age += 1 
    
    def setLifeSpan(self): 
        '''
        upon arrival to destination, package is assumed delivered, its "destroyed" conceptually
        by setting its _LIFE_SPAN to its current age. 
        '''
        self._LIFE_SPAN = self.age
        
    def getLifeSpan(self):
        '''
        accesor function for package life span 
        '''
        return self._LIFE_SPAN
    