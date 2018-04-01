# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Riko
"""

import random 
import uuid 

from queue import Queue

from parcel import Parcel 

class ParcelQueue():
    '''
    A Parcel queue class.
    The class has the following attributes:
        queue_(queue.Queue) where all parcel objects are queued
        SOURCE (str) airport name
        DESTINATION (str) airport name
        
    '''
    def __init__(self, model, source_name, destination_name, pdf_params = None):
        '''
        Create a parcel agent.
        Args:
            source_name - the airport this queue is instantiated in 
            destination_name - the destination airport this queue is assigned to
            pdf_params - probability distribution function type and parameters 
                for parcel generation #TODO
                
        '''
        #super().__init__(unique_id, model)
        self.model = model
        self.SOURCE = source_name
        self.DESTINATION = destination_name
        self.queue_ =  Queue() # The parcel queue 

    def generate_parcels(self,number=1):
        '''
        generates parcels within the queue based on probability density function
        FOR NOW implemented as 80% chance a parcel is created 
        '''    
        for i in range(number):
            if random.random() > 0.2:
                #print("{}. {} appears {} times.".format(i, key, wordBank[key]))
                print("Creating parcel in {} destined to {}".format(self.SOURCE, self.DESTINATION))
                p = Parcel(uuid.uuid4(),
                           self.model,
                           self.SOURCE,
                           self.DESTINATION)
                self.queue_.put(p)
                self.model.schedule.add(p)
                
    def get_size(self):
        '''
        returns the number of parcels in the queue 
        '''
        return len(self.queue_.queue)

    def get_parcels(self, mass_limit): 
        '''
        returns a list of parcels and their total mass [payload] for shipment that weigths no more than [mass_limit] and removed from queue 
        '''
        
        # TODO: change implementation to something more elegant.
        # will be nicer once use collections.deque instead of queue.Queue 
        
#        print ("This queue has {} parcels".format(self.get_size()))
        shipment = list()
        shipment_mass = 0.0
        shipment_size   = 0
        for i in range(self.get_size()): 
#            print ("i=",i)
            temp = shipment_mass + self.queue_.queue[i].MASS 
            if temp < mass_limit :
                shipment_mass += self.queue_.queue[i].MASS 
#                print ("Added package number {}, whose weight is {}, shipment weight: {}".format(i, self.queue_.queue[i].WEIGHT, shipment_weight))
                shipment_size += 1
        
        print ("shipment size is {} parcels".format(shipment_size))
        for i in range(shipment_size): 
            shipment.append(self.queue_.get()) #Remover from queue and append to shipment
        
#        print (shipment_weight)
        return shipment, shipment_mass

    
#    def step(self):
#        '''
#        Not sure this is best implemented as an agent. Might make more sense for 
#        it to be a container class for parcel agents only. 
#        '''
#        pass
        
    