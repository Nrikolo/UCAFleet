# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:45:46 2018

@author: Riko
"""

#model.py file 

#Contains the model class. 
#If the file gets large, 
#it may make sense to move the complex bits into other files, 
#but this is the first place readers will look to figure out how the model works.

#SEEDING 
#def __init__(self, seed=None):
#        super().__init__(seed)
#        # ...

#model = AwesomeModel(seed=1234)


'''
Fleet
=============================================================
A Mesa implementation of an aerial delivery network.
Uses numpy arrays to represent vectors.
'''


import random
import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from uav import Uav
from airport import Airport
import uuid
#Should the parcel be another type of agent? 
#TODO: make consistent naming of functions and variables!!!! 


class Fleet(Model):
    '''
    Fleet model class. Handles agent creation, placement and scheduling.
    Attributes: 
        Airports : a dictionary of name (string) and position (x,y) in km 
        UAVs: Define number of UAVs in model and their initial spawning
        width, height: should be derived from airport locations, of the space
        steps_per_hour: the number of steps per hour unit of time (60 means the
        step size is one minute)
        
    '''
    
    def __init__(self,
                 airports,
                 num_uavs,
                 steps_per_hour,
                 width=500,
                 height=500):
        '''
        Create a new Fleet model.
        Args:
            airports: a pandas DataFrame with airport name ,  location , 
                probability density function parameters and refuelingRate
                {name, x, y, pdfParams ,refuelingRate}
            num_uavs: the total number of UAVs in model (distribution is sort of random uniform for now)
            steps_per_hour: the number of steps per hour unit of time
            width, height: Size of the space.
        '''
        self._AIRPORTS = airports
        self._NUM_UAVS = num_uavs
        self._STEPS_PER_HOUR = steps_per_hour
     
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.parcel_aggregator = list()
        self.make_agents()
        self.running = True

    def getStepsPerHour(self): 
        return self._STEPS_PER_HOUR
    
    def make_airports(self):
        '''
        '''
        
        #for index, row in df.iterrows():
        #    print row['c1'], row['c2']
        #TODO have a type designation in agents 
        for index,row in self._AIRPORTS.iterrows():
            airport = Airport(uuid.uuid4(),self,index,(row('x'),row('y')),row['refuelingRate'] ,row['pdf_params'])
            self.schedule.add(airport)
        
        
    def make_uavs(self):
        '''
        '''
        for index,row in self._AIRPORTS.iterrows():
            airport = Airport(uuid.uuid4(),self,index,(row('x'),row('y')),row['refuelingRate'] ,row['pdf_params'])
            self.schedule.add(airport)
        
        
        for i in range(self.num_uavs):
            
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            uav = Uav(uuid.uuid4(), self, pos, self.speed, velocity,
                        self.separation, **self.factors)
            self.space.place_agent(uav, pos)
            self.schedule.add(uav)
        
    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''
        self.make_airports()
        self.make_uavs()
        
    
    def getRandomDestinationAirport(self,source_name): 
        '''
        pulls a random airport from the available airports not including the source airport name
        '''
        
        random_airport_name = random.choice(self.airports).NAME
        while (random_airport_name == source_name):
            random_airport_name = random.choice(self.airports).NAME
        return random_airport_name 
    
    def step(self):
        self.schedule.step()