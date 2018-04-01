# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Riko
"""

import numpy as np
from queue import Queue

from mesa import Agent


class ParcelQueue():
    '''
    A Parcel queue class.
    The class has the following attributes:
        queue_(queue.Queue) where all parcel objects are queued
        SOURCE (str) airport name
        DESTINATION (str) airport name
        
    '''
    def __init__(self, source_name, destination_name, pdf_params = None):
        '''
        Create a parcel agent.
        Args:
            source_name - the airport this queue is instantiated in 
            destination_name - the destination airport this queue is assigned to
            pdf_params - probability distribution function type and parameters 
                for parcel generation #TODO
                
        '''
        #super().__init__(unique_id, model)
        self.SOURCE = source_name
        self.DESTINATION = destination_name
        self.queue_ =  Queue() # The parcel queue 
            
    def get_parcels(self, mass_limit): 
        '''
        returns a list of parcels and thier total mass [payload] for shipment that weigths no more than [mass_limit] and removed from queue 
        '''
        # TODO: implement only taking the oldest parcels that amount to no more than
        # the mass_limit. 
        
        # Entire queue is to be shipped 
        shipment = list(self.queue_.queue) # Cast to list and assign to shipment
        
        with self.queue_.mutex:
            self.queue_.queue.clear()  # Clear the queue of the parcels taken for shipment        
        return shipment                     

#    def step(self):
#        '''
#        Not sure this is best implemented as an agent. Might make more sense for 
#        it to be a container class for parcel agents only. 
#        '''
#        pass
        
    