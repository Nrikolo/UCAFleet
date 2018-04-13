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
        source_name (str): airport name where the parcel is from
        destination_name (str): airport name where the parcel is destined to
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
        self.source_name = source_name
        self.destination_name = destination_name
        self.q = deque()

    def generate_parcels(self,number=1):
        '''
        generates parcels within the queue based on probability density function
        
        Note: 
            FOR NOW implemented as 100% chance a parcel is created 

        Args:
            number (int): the number of parcels to generate
        '''    
        for i in range(number):
            if random.random() > 0.0:
                #TODO: modify to use pdf_params instead of hard coded value
                p = Parcel(uuid.uuid4(),
                           self.model,
                           self.source_name,
                           self.destination_name)
                self.q.append(p)
                self.model.schedule.add(p)
                
    def get_size(self):
        '''
        returns the number of parcels in the queue 
        '''
        return len(self.q)
    
    def get_mass(self):
        '''
        returns the total mass of parcels in the queue 
        '''
        mass = 0
        for i in range(self.get_size()): 
#            print ("i=",i)
            mass += self.q[i].MASS 
        
        return mass

    def get_avg_age(self): 
        '''
        returns the average age of parcels in the queue
        '''
        total_age = 0
        for i in range(self.get_size()):
            total_age += self.q[i].age
        
        return total_age / self.get_size()
        
    def get_shipment(self, min_mass=200, mass_limit=500): 
        '''
        returns the number of parcels and their total mass [payload] for shipment 
        that weigths no more than [mass_limit] from the begining of the queue
        
        '''
        
        shipment_mass = 0.0
        shipment_size   = 0
        
        # TODO: change implementation to something more elegant.
        
        if self.get_mass() < min_mass :
            return shipment_size, shipment_mass  # Not enough payload to justify loading
            
        print ("This queue has {} parcels".format(self.get_size()))
        
        for i in range(self.get_size()): 
#            print ("i=",i)
            temp = shipment_mass + self.q[i].MASS 
            if temp < mass_limit:
                shipment_mass += self.q[i].MASS 
#                print ("Added package number {}, whose weight is {}, shipment weight: {}".format(i, self.queue_.queue[i].WEIGHT, shipment_weight))
                shipment_size += 1
      
        print ("This shipment has {} parcels weighing a total of {}".format(shipment_size,shipment_mass))

        return shipment_size, shipment_mass

    def remove_parcels(self,shipment_size):
        '''
        removes shipment_size number of parcels from the queue as they are loaded
        onto a uav at the home airport
        '''
        shipment = list() 
        print ("shipment size is {} parcels".format(shipment_size))
        for i in range(shipment_size): 
            shipment.append(self.q.popleft()) #Remove from queue and append to shipment
            
        return shipment

        
    