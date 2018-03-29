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



class Fleet(Model):
    '''
    Fleet model class. Handles agent creation, placement and scheduling.
    Attributes: 
        Airports : a dictionary of name (string) and position (x,y) in km 
        UAVs: Define number of UAVs in model and their initial spawning
        width, height: should be derived from airport locations, of the space
        steps_per_hour: the number of steps per hour unit of time (60 means the step size is one minute)
        
        
        
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
            airports: a pandas DataFrame with airport name and location
            num_uavs: the total number of UAVs in model (distribution is sort of random uniform for now)
            
            width, height: Size of the space.
        '''
        self.num_uavs = num_uavs
        self.steps_per_hour = steps_per_hour
     
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        
        self.make_agents()
        self.running = True

    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''
        for i in range(self.num_uavs):
            
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            boid = Uav(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, **self.factors)
            
            
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)
        
        #TODO have a type designation in agents 
        for i in model.airports.shape[0]
            airport = Airport(i, self, ...)

    def step(self):
        self.schedule.step()