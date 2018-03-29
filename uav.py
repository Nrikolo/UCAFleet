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
        - ONROUTE: flying from source to destination 
        - REFUEL: after landing, the turnaround time minimum, as if refueling
        - IDLE: UAV is ready to transport but hasn't been issued a mission thus
            it is idle.
   
    The UAV has the following attributes:
        UUID: static, the UAV unique idnetified (like tail number)
        MAX_PAYLOAD (400kg): static, maximal amount of payload the UAV can carry
        MIN_PAYLOAD (200kg): static, the minimal amount of payload for it to 
            take off
        SPEED (278kph): static, UAV speed (velocity magnitude) , 150kts
        MAX_RANGE (2100km): static, the maximum distance (source->desitnation)
            the UAV can fly (7.4 hours max)
        FUEL_CAPACITY (300L): static, the maximum colume of fuel the UAV can hold 
        FUEL_CONSUMPTION (38L/hr): static, the nominal fuel consumption rate at
            60% power, 10kft, 150kts
        payload (int): The loaded payload on the UAV, basically the total weight
            of packages 
        packages (queue): the packages on board the UAV 
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
    FUEL_CAPACITY = 300 #Liters
    FUEL_CONSUMPTION = 38 #Liters/hr
        
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
        ##TODO: fix this, model doesn't have airports as attribute
        self.pos = model.airports.loc[self.source_name].values
        self.packages = list()
        self.payload = 0
        self.destination_name = None
        self.fuel = self.FUEL_CAPACITY #instantiated with full tank of gas 
        self.odometer = 0
        self.num_landings = 0 
        self.STATE = 'IDLE'

    
    def finished_refueling(self): 
        #Ensure no overflow of fuel
        self.fuel = self.FUEL_CAPACITY
        #UAV is now waiting to be loaded, state change to IDLE
        self.STATE = 'IDLE'
        
    def finished_loading(self): 
        self.STATE = 'ONRAOUTE'
        
    def unload(self): 

        #move them to "aggragator"
        self.model.package_aggregator += self.packages
        #unload packages by clearing the list        
        self.packages[:] = []
        
        
    def reached_destination(self):
        #UAV has landed
        #UAV is unloaded at destination
        self.unload()
        #change state to refueling 
        self.STATE = 'REFUELING'
        
    def try_loading(self): 
        '''
        returns true if loading was succesful and false otherwise 
        '''
        
        #TODO: implement as a public method of the airport the uav is in
        self.packages = list(self.model.airports.loc[self.source_name].load_uav(self))
        return self.packages
        

    def step(self):
        '''
        Get the UAV's state, compute the next action 
        '''
        if self.STATE == 'OnRoute':
            #If uav is onroute to its destination, continue until reached
            
            ##TODO: can be done more efficiently if destination pose is stored? 
            destination_pose = self.model.airports.loc[self.destination_name].values
            #Distance to destination
            distance_to_destination = self.model.space.get_distance(self.pos,
                                                                    destination_pose )
            #TODO: might make sense to have this as an attribute since its not changing 
            distance_per_step = self.SPEED/(self.model.getStepsPerHour())
            
            #If the distance left to reach destination is less than what the UAV 
            #will cover in this step, it has reached the destination
            
            #TODO: Make this section more elegant 
            if distance_to_destination > distance_per_step :
                #Haven't reached the destination, keep going...
                
                #The translation vector             
                error_vector = self.model.space.get_heading(self.pos,
                                                            destination_pose )
                #Heading vector is obtained by normalizing (unit vector)
                heading_vector = error_vector/ distance_to_destination     
                #Compute the new position by adding the translation vector to 
                #the old position
                new_position = self.pos + distance_per_step * heading_vector
                #Add the distance traveled to the odometry
                self.odometer += distance_per_step
                #Decrement the fuel available on UAV 
                self.fuel -= self.FUEL_CONSUMPTION / (self.model.getStepsPerHour())
                
            else:
                #Reached destination! 
                #Force empty fuel 
                #TODO: remove this force reset 
                self.fuel = 0.0 
                #set new position to be the destination
                new_position = destination_pose
                #add actual distance to odometer
                self.odometer += distance_to_destination
            
            #TODO: decrement fuel 
            
            #Move the agent to the new position
            self.model.space.move_agent(self, new_position)
            

        if self.STATE == 'REFUEL':
            #If uav is refueling, continue until full
            
            if self.fuel < self.FUEL_CAPACITY:
                #TODO: get the REFUELING_SPEED from the current airport 
                #(self.SOURCE) the UAV is in
                #self.fuel += self.model.airports.loc[self.SOURCE].values
                self.fuel += 30
            else:
                self.finished_refueling()
                
        if self.STATE == 'IDLE' and self.try_loading(): 
            #Assumes that loading takes 1 step
            #TODO: consider adding a "LOADING" State for UAV if it is to take 
            #more than one step
            self.finished_loading()
                
               
        #If Idle
        
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity += (self.cohere(neighbors) * self.cohere_factor +
                          self.separate(neighbors) * self.separate_factor +
                          self.match_heading(neighbors) * self.match_factor) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)
        
# =============================================================================
# Reference functions from example code        
# =============================================================================
        
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
