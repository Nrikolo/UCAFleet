# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:33:13 2018

@author: Riko
"""

#import numpy as np
from collections import defaultdict

from mesa import Agent
from airport import Airport 
#from parcel import Parcel

class Uav(Agent):
    '''
    A UAV agent.
    The agent has three states:
        - ONROUTE: flying from source to destination 
        - REFUELLING: after landing, the turnaround time minimum, as if refuelling
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
            of parcels 
        parcels (queue): the parcels on board the UAV 
        source (airport NAME, str): The UAV flight source
        destination (airport NAME, str): The UAV flight desitnation 
        position: UAV current position in x,y coordinates in km  
        fuel: The amount of liters of fuel the UAV has 
        odometer: The total distance the UAV has traveled 
        num_landings: The number of landings the UAv has conducted
    '''
    
    MAX_PAYLOAD   = 400 #kg
    # TODO: change min payload to 200kg
    MIN_PAYLOAD   = 200 #kg 
    SPEED         = 278 #kph
    MAX_RANGE     = 2300 #km
    FUEL_CAPACITY = 300 #Liters
    FUEL_CONSUMPTION = 38 #Liters/hr
    
    name_index = defaultdict(list)

    def __init__(self, unique_id, model, airportObj):
        '''
        Create a new UAV agent.
        Args:
            unique_id: Unique agent identifier.
            model: the model 
            airport_name: where the uav is instantiated
        '''
        print("Creating a uav instance with id {} in airport {}".format(unique_id, airportObj.name))
        super().__init__(unique_id, model)
        
        # TODO: Figure out if this is redundent 
        # since space.place_agent() sets the agent position already
        #"Private"
        self._parcels = list()
        self._payload = 0
        self._odometer = 0.0
        self._STATE = 'IDLE'
        #"Public"
        self.pos = airportObj.pos 
        self.type_ = 'uav'
        self.source_name = airportObj.name
        self.num_landings = 0 
        self.destination_name = None
        self.fuel = self.FUEL_CAPACITY #instantiated with full tank of gas 
        
        Uav.name_index[self.unique_id].append(self)

        
    @classmethod
    def find_by_name(cls,name): 
        return Uav.name_index[name]
    
# =============================================================================
#     Pseudo private methods 
# =============================================================================
    def _set_destination(self, destination=None):
        '''
        Sets destination of UAV 
        '''
        self.destination_name = destination
        
    
    def _set_source(self, source):
        '''
        Sets source of UAV 
        '''
        self.source_name = source    
        
    
    def _finished_refuelling(self): 
        '''
        Sets the fuel task to max capacity and changes state of uav to IDLE 
        '''
        print("UAV {} finished refuelling".format(self.unique_id))
        self.fuel = self.FUEL_CAPACITY  # Ensure no overflow of fuel
        self._STATE = 'IDLE'  # UAV is now waiting to be loaded, state change to IDLE
        
    
    def _finished_loading(self): 
        '''
        a state change for uav so that in the next time step it would progress to wards its destination
        '''
        self._STATE = 'ONROUTE' # Since uav finished loading, it should be ready for takeoff
        # Remove this uav from the airport's queue
        Airport.find_by_name(self.source_name)[0].release_uav(self)
        
        
    def _update_payload(self, mass=None): 
        '''
        updates uav payload [kg] based on the current parcels loaded
        '''
        
        if mass is None:
            for p in self._parcels:
                self._payload += p.MASS
        else: 
            self._payload = mass
        
            
    def _reached_destination(self):
        '''
        uav has reached its destination, function unloads UAV and changes its 
        state to refuelling
        '''
        #UAV has reached destination and landed
        print("UAV {} has reached {}".format(self.unique_id,
                                             self.destination_name))
        #change state to refuelling 
        self._STATE = 'REFUELLING'
        
        # Set source to what was the destination 
        self._set_source(self.destination_name)
        
        # Erase destination (will be filled by airport once uav is loaded)
        self._set_destination(None)
        
        self.num_landings += 1  #UAV has landed once more
        
        # Add UAV to airport uav_queue with the new source name (where uav is now)
        Airport.find_by_name(self.source_name)[0].store_uav(self)
        
   

# =============================================================================
# pseudo public methods 
# =============================================================================

    def is_IDLE(self):
        return self.get_state() is 'IDLE'
    
    def is_REFUELLING(self):
        return self.get_state() is 'REFUELLING'
    
    def is_ONROUTE(self):
        return self.get_state() is 'ONROUTE'
    
    def get_state(self): 
        return self._STATE
    
    def is_loaded(self): 
        if self.get_parcels():
            return True
        else:
            return False
        
    def get_parcels(self): 
        return self._parcels
    
    def unload(self): 
        '''
        unloads uav parcels by deleting the parcels and updating the payload 
        '''
    
        self._parcels = []  # Unload parcels by clearing the list of parcels on the uav      
        self._update_payload() # Update the payload mass of the uav
        print("{} unloaded, no parcels onboard".format(self.unique_id))
        
        
    def load(self, shipment, destination, mass=None):
        '''
        loads uav with shiptment menifest and sets destination in packages and uav
        '''
        #set transporter in all parcels in list 
        print("\n In Load method of UAV {}, loading {} destined to {} ".format(self.unique_id, shipment, destination))
        for p in shipment:
            p.set_transporter(self) 
        #TODO: obtain the destination from the parcels and validate they are all destined to the same location
        self._parcels = shipment    
        self._set_destination(destination)  # TODO: should be deduced from the shipment? 
        self._update_payload(mass)
        self._finished_loading()        


    def step(self):
        '''
        Get the UAV's state, compute the next action 
        '''
        print("In step method of UAV {}".format(self.unique_id))
        if self.is_ONROUTE():
            print("UAV {} is flying from {} to {}".format(self.unique_id, 
                                                          self.source_name,
                                                          self.destination_name))
#            print("fuel :", self.fuel)
            #If uav is onroute to its destination, continue until reached
            
            ##TODO: can be done more efficiently if destination pose is stored? 
            destination_pose =  Airport.find_by_name(self.destination_name)[0].pos
#            print("destination_pose :", destination_pose)
            #Distance to destination
            distance_to_destination = self.model.space.get_distance(self.pos,
                                                                    destination_pose )
#            print("distance_to_destination :", distance_to_destination)

            #TODO: might make sense to have this as an attribute since its not changing 
            distance_per_step = self.SPEED/(self.model.get_steps_per_hour())
            
            #If the distance left to reach destination is less than what the UAV 
            #will cover in this step, it has reached the destination
            
            #TODO: Make this section more elegant 
            if distance_to_destination > distance_per_step :
                #Haven't reached the destination, keep going...
                
                #The translation vector             
                error_vector = self.model.space.get_heading(self.pos,
                                                            destination_pose)
#                print("error vector:", error_vector)
                #Heading vector is obtained by normalizing (unit vector)
                heading_vector = error_vector/ distance_to_destination     
#                print("heading_vector :", heading_vector)

                #Compute the new position by adding the translation vector to 
                #the old position
                new_position = self.pos + distance_per_step * heading_vector
#                print("new_position :", new_position)

                #Add the distance traveled to the odometry
                self._odometer += distance_per_step
#                print("self._odometer: ",self._odometer)
                #Decrement the fuel available on UAV 
                self.fuel -= self.FUEL_CONSUMPTION / (self.model.get_steps_per_hour())
            else:
                #Reached destination! 
                new_position = destination_pose  # Set new position to be the destination
                self._odometer += distance_to_destination  # Add actual distance to odometer
                self._reached_destination() 
                
            
            #Move the agent to the new position
            self.model.space.move_agent(self, new_position)
            return

        if self.is_REFUELLING():
            #If uav is refuelling, continue until full
            print("UAV {} is at {} refuelling. Current content is {} liters".format(self.unique_id,
                                                                                    self.source_name,
                                                                                    self.fuel))
            if self.fuel < self.FUEL_CAPACITY:
                self.fuel += Airport.find_by_name(self.source_name)[0].refuelling_rate
                #https://stackoverflow.com/questions/10858575/find-object-by-its-member-inside-a-list-in-python
            else:
                self._finished_refuelling()
            return 
             
        if self.is_IDLE():
            print("UAV {} is at {} idle.".format(self.unique_id,
                                                 self.source_name))
            pass
            #Assumes that loading takes 1 step
        
                
               
        