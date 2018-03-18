# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:33:13 2018

@author: Riko
"""

import numpy as np

from mesa import Agent


class Uav(Agent):
    '''
    A UAV agent.
    The agent has three states:
        - OnRoute: flying from source to destination 
        - ReFuel: after landing, the turnaround time minimum, as if refueling
        - Idle: UAV is ready to transport but hasn't been issued a mission thus it is idle.
   
    The UAV has the following attributes:
        UUID: static, the UAV unique idnetified (like tail number)
        MAX_PAYLOAD (400kg): static, maximal amount of payload the UAV can carry
        MIN_PAYLOAD (200kg): static, the minimal amount of payload for it to take off
        SPEED (278kph): static, UAV speed (velocity magnitude)
        MAX_RANGE (2300km): static, the maximum distance (source->desitnation) the UAV can fly
        FUEL_CAPACITY (302L): static, the maximum colume of fuel the UAV can hold 
        payload (int): The loaded payload on the UAV
        source (airport NAME, str): The UAV flight source
        destination (airport NAME, str): The UAV flight desitnation 
        position: UAV current position in x,y coordinates in km  
        fuel: The amount of liters of fuel the UAV has 
        odometer: The total distance the UAV has traveled 
        num_landings: The number of landings the UAv has conducted


    '''
    MAX_PAYLOAD   = 400 #kg
    MIN_PAYLOAD   = 200 #kg
    SPEED         = 278 #kph
    MAX_RANGE     = 2300 #km
    FUEL_CAPACITY = 302 #Liters
        
    def __init__(self, unique_id, model, airport_name):
        '''
        Create a new UAV agent.
        Args:
            unique_id: Unique agent identifier.
            model: the model 
            airport_name: where the uav is instantiated
        '''
        super().__init__(unique_id, model)
        self.source_name = airport_name
        self.position = model.airports.loc[self.source_name].values
        self.payload = 0
        self.destination_name = None
        self.fuel = self.FUEL_CAPACITY #instantiated with full tank of gas 
        self.odometer = 0
        self.num_landings = 0 
        self.STATE = 'Idle'

    def cohere(self, neighbors):
        '''
        Return the vector toward the center of mass of the local neighbors.
        '''
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        '''
        Return a vector away from any neighbors closer than separation dist.
        '''
        me = self.pos
        them = (n.pos for n in neighbors)
        separation_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation:
                separation_vector -= self.model.space.get_heading(me, other)
        return separation_vector

    def match_heading(self, neighbors):
        '''
        Return a vector of the neighbors' average heading.
        '''
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
        return match_vector

    def finished_refueling(self): 
        self.STATE = 'Idle'
        
    def finished_loading(self): 
        self.STATE = 'OnRoute'
    
    def try_loading(self): 
        '''
        UAV loops through source queues and selects a set of packages to load 
        it will be succesful if there are more than MIN_PAYLOAD packages for one destination 
        UAV will take the oldest packages , up to MAX_PAYLOAD to destination 
        #TODO: figure out package prioritization (what is older queue??)
        
        '''
    
    def step(self):
        '''
        Get the UAV's state, compute the next action 
        '''
        if self.STATE == 'OnRoute':
            destination_pose = self.model.airports.loc[self.destination_name].values
            #Distance to destination
            travel_to_go = self.model.space.get_distance(self.position, destination_pose )
            #The translation vector 
            travel_dist_vect = self.SPEED/(self.model.steps_per_hour) * self.model.space.get_heading(self.position, destination_pose )
            travel_dist = np.linalg.norm(travel_dist_vect)
            # if the distance left to reach destination is less than what the UAV 
            #will cover in this step, it has reached the destination
            if travel_to_go < travel_dist:
                #Reached destination! 
                new_position = destination_pose
                self.odometer += travel_to_go
            else:
                #Compute the new position by adding the translation vector to the old position
                new_position = self.position + travel_dist_vect
                #Add the distance traveled to the odometry
                self.odometer += travel_dist 
            
            #Move the agent to the new position
            self.model.space.move_agent(self, new_position )

        if self.STATE == 'ReFuel':
            if self.fuel < self.FUEL_CAPACITY:
                self.fuel += 100
            else:
                self.finished_refueling()
        if self.STATE == 'Idle' and self.try_loading(): 
            self.finished_loading()
                
                

                
        #If Idle
            #Check payload>MIN_PAYLOAD -> assign destination and switch to OnRoute
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity += (self.cohere(neighbors) * self.cohere_factor +
                          self.separate(neighbors) * self.separate_factor +
                          self.match_heading(neighbors) * self.match_factor) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)