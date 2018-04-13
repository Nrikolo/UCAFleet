# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Nir Rikovitch
"""

import numpy as np
from mesa import Agent


class Parcel(Agent):
    '''
    A Parcel class representing a package/parcel meant for shipment
    
    This Parcal class inherits from the mesa agent class and behaves as 
    a passive agent. Meaning, it is handled by other classes from being 
    instanciated, loaded, moved and destroyed. 
    
    Attributes: 
        UUID (uuid): a unique identifier for this parcel  
        model (:obj:'Fleet'): an instance of class 'Fleet' representing the model
        pdf_params (?): probability density function parameters for parcel mass the volume generation
        MASS (float): the mass of the parcel [kg]
        VOLUME (float): the metric volume of the parcel [m^3] 
        SOURCE (str): airport name where the parcel is from
        DESTINATION (str): airport name where the parcel is destined to
        TRANSPORTER (uuid): the uav uuid that has transported this parcel
        _LIFE_SPAN (int): the total time (number of steps): the parcel existed prior to reaching its desitnation
        age (int): the total time the parcel exists from inception till now
    '''
    
    def __init__(self, unique_id, model, source_name, destination_name, pdf_params = None):
        '''
        Create a parcel agent.
        Args:
            see class documentation 
        '''
        super().__init__(unique_id, model)
        # "Private"
        self._LIFESPAN = None 
        self._TRANSPORTER = None # UUID of transporting uav
        
        # "Public"
        self.type_ = 'parcel'
        self.source_name = source_name
        self.destination_name = destination_name
        #TODO: use random.choice(self.model.schedule.agents) 
        #would require implementing a custom scheduler with 2 types of agents
        #this would select a random agent (airport) from the list of available airports excluding the input 
        
        self.MASS = round(2.5 * np.random.randn() + 10,2)
        self.VOLUME = round(2.1 * np.random.randn() + 1,2)
        self.age = 0
        print("A parcel of mass {} kg and volume {} m^3 was instantiated in {} destined to {}".format(self.MASS, self.VOLUME, self.source_name, self.destination_name))

        
# =============================================================================
#     pseudo private methods
# =============================================================================
        
    def _increment_age(self): 
        '''
        Increments the age of the parcel by a single step 
        '''
        self.age += 1 

# =============================================================================
#     pseudo public methods
# =============================================================================
    
    def set_transporter(self,uavObj):
        '''
        accessor to set the uav that transports this parcel
        '''
        self._TRANSPORTER = uavObj.unique_id
        
        
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
   
    def parcel_mass():
        pass
        
    def parcel_volume():
        pass        
    
    def step(self):
        '''
        Implements the step method of the agent of type parcel by aging it one step.
        '''
        self._increment_age()
        
    