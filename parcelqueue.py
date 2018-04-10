# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:14 2018

@author: Riko
"""

import random 
import uuid 
from collections import deque 

from parcel import Parcel 

class ParcelQueue():
    '''
    A parcel queue in an airport meant for shipment to another single destination
    
    This queue is a generalized container deque class that stores parcel 
    instances in order of instanciation meant for a single destination (another airport). 
    It implements methods for generating parcels, getting a shipment for loading
    
    Attributes: 
        model (:obj:'Fleet'): an instance of class 'Fleet' representing the model
        pdf_params (?): probability density function parameters for parcel generation
        queue_(deque) where all parcel objects are queued    
        SOURCE (str): airport name where the parcel is from
        DESTINATION (str): airport name where the parcel is destined to
    '''
    
    def __init__(self, model, source_name, destination_name, pdf_params = None):
        '''
        Create a parcel queue 
        
        Args:
            model
            source_name
            destination_name
            pdf_params
        '''
        #super().__init__(unique_id, model)
        self.model = model
        self.SOURCE = source_name
        self.DESTINATION = destination_name
        self.q = deque()

    def generate_parcels(self,number=1):
        '''
        generates parcels within the queue based on probability density function
        
        Note: 
            FOR NOW implemented as 80% chance a parcel is created 

        Args:
            number (int): the number of parcels to generate
        '''    
        for i in range(number):
            if random.random() > 0.2:
                #TODO: modify to use pdf_params instead of hard coded value
                print("Creating parcel in {} destined to {}".format(self.SOURCE, self.DESTINATION))
                p = Parcel(uuid.uuid4(),
                           self.model,
                           self.SOURCE,
                           self.DESTINATION)
                self.q.append(p)
                self.model.schedule.add(p)
                
    def get_size(self):
        '''
        returns the number of parcels in the queue 
        '''
        return len(self.q)

    def get_shipment(self, mass_limit): 
        '''
        returns a list of parcels and their total mass [payload] for shipment that weigths no more than [mass_limit] and removed from queue 
        '''
        
        # TODO: change implementation to something more elegant.
        # will be nicer once use collections.deque instead of queue.Queue 
        
#        print ("This queue has {} parcels".format(self.get_size()))
        shipment = list()
        shipment_mass = 0.0
        shipment_size   = 0
        for i in range(self.get_size_()): 
#            print ("i=",i)
            temp = shipment_mass + self.q[i].MASS 
            if temp < mass_limit:
                shipment_mass += self.q[i].MASS 
#                print ("Added package number {}, whose weight is {}, shipment weight: {}".format(i, self.queue_.queue[i].WEIGHT, shipment_weight))
                shipment_size += 1
        
        print ("shipment size is {} parcels".format(shipment_size))
        for i in range(shipment_size+1): 
            shipment.append(self.q.popleft()) #Remove from queue and append to shipment
        
#        print (shipment_weight)
#        for i in xrange(4096):
#            C.append(A.popleft())

#        shipment = list(itertools.islice(self.queue_,0,last_item_to_take))
        return shipment, shipment_mass

    
#    def step(self):
#        '''
#        Not sure this is best implemented as an agent. Might make more sense for 
#        it to be a container class for parcel agents only. 
#        '''
#        pass
        
    