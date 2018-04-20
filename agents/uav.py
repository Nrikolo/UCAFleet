# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:33:13 2018

@author: Riko
"""
import numpy as np
from flight import Flight
from collections import defaultdict

from mesa import Agent
from agents.airport import Airport

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

    MAX_PAYLOAD = 400 #kg
    MIN_PAYLOAD = 20 #kg
    SPEED = 278 #kph
    MAX_RANGE = 2300 #km
    FUEL_CAPACITY = 300 #Liters
    FUEL_CONSUMPTION = 38 #Liters/hr

    name_index = defaultdict(list)

    def __init__(self, unique_id, model, airport_obj):
        '''
        Create a new UAV agent.
        Args:
            unique_id: Unique agent identifier.
            model: the model
            airport_name: where the uav is instantiated
        '''
        print("[SPAWN] Creating a uav instance with id {} in " \
              "airport {}".format(unique_id, airport_obj.name))
        super().__init__(unique_id, model)

        #"Private"
        self._parcels = list()
        self._payload = 0
        self._odometer = 0.0  # km
        self._tfh = 0.0  # hours
        self._STATE = 'IDLE'
        self._flight_steps_duration = 0
        #"Public"
        self.pos = airport_obj.pos
        self.heading = np.array([0,0])
        self.type_ = 'uav'
        self.source_name = airport_obj.name
        self.num_landings = 0
        self.destination_name = None
        self.fuel = self.FUEL_CAPACITY #instantiated with full tank of gas
        self.logger = list() # A flight log book 
        
        Uav.name_index[self.unique_id].append(self)


    @classmethod
    def find_by_name(cls, name):
        '''
        enables query by name at the class level
        '''
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
#        print("UAV {} finished refuelling".format(self.unique_id))
        self.fuel = self.FUEL_CAPACITY  # Ensure no overflow of fuel
        self._STATE = 'IDLE'  # UAV is now waiting to be loaded, state change to IDLE


    def _finished_loading(self):
        '''
        a state change for uav so that in the next time step it would progress
        to wards its destination
        '''
        self._STATE = 'ONROUTE' # Since uav finished loading, it should be ready for takeoff
        # Remove this uav from the airport's queue
        Airport.find_by_name(self.source_name)[0].release_uav(self)
        print("[ONROUTE] UAV {} is flying from {} to {}".format(self.unique_id,
                                                                self.source_name,
                                                                self.destination_name))
#           


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
        print("[ARRIVAL] UAV {} has reached {}".format(self.unique_id,
                                                       self.destination_name))
        #change state to refuelling
        self._STATE = 'REFUELLING'
        distance = self.model.space.get_distance(Airport.find_by_name(self.source_name)[0].pos,
                                                 Airport.find_by_name(self.destination_name)[0].pos)
        # TODO: compute the flight duration and update the logger
        self.logger.append(Flight(self.source_name,
                                  self.destination_name, 
                                  distance,
                                  self._flight_steps_duration / self.model.get_steps_per_hour(),
                                  self.get_payload_mass(),
                                  self.FUEL_CAPACITY-self.fuel))
        # Set source to what was the destination
        self._set_source(self.destination_name)

        # Erase destination (will be filled by airport once uav is loaded)
        self._set_destination(None)

        self.num_landings += 1  #UAV has landed once more
        self._flight_steps_duration = 0 # Reset flight time counter 
        # Add UAV to airport uav_queue with the new source name (where uav is now)
        Airport.find_by_name(self.source_name)[0].store_uav(self)

# =============================================================================
# pseudo public methods
# =============================================================================

    def is_IDLE(self):
        '''
        checks if uav is idle, returns true if IDLE
        '''
        return self.get_state() is 'IDLE'

    def is_REFUELLING(self):
        '''
        checks if uav is refuelling, returns true if REFUELLING
        '''
        return self.get_state() is 'REFUELLING'

    def is_ONROUTE(self):
        '''
        checks if uav is onroute, returns true if ONROUTE
        '''
        return self.get_state() is 'ONROUTE'

    def get_state(self):
        '''
        Accessor method to get the uav state
        '''
        return self._STATE

    def is_loaded(self):
        '''
        checks if uav is loaded and returns true is so
        '''
        return bool(self.get_parcels())

    def get_parcels(self):
        '''
        accessor for uav parcels
        '''
        return self._parcels

    
    def get_payload_qty(self):
        '''
        accessor for uav payload qty
        '''
        return len(self._parcels)
    
    def get_payload_mass(self):
        '''
        accessor for uav payload mass
        '''
        return self._payload


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
#        print("\n In load method of UAV {}, loading {} destined to {} ".format(self.unique_id,
#                                                                               shipment,
#                                                                               destination))
        for p in shipment:
            p.set_transporter(self)
        # TODO: obtain the destination from the parcels and validate they
        #are all destined to the same location
        self._parcels = shipment
        self._set_destination(destination)
        self._update_payload(mass)
        self._finished_loading()


    def step(self):
        '''
        Get the UAV's state, compute the next action
        '''
        if self.is_ONROUTE():
            self._flight_steps_duration += 1 
#            print("[ONROUTE] UAV {} is flying from {} to {}".format(self.unique_id,
#                                                                    self.source_name,
#                                                                    self.destination_name))

            #If uav is onroute to its destination, continue until reached
            destination_pose = Airport.find_by_name(self.destination_name)[0].pos
            #Distance to destination
            distance_to_destination = self.model.space.get_distance(self.pos,
                                                                    destination_pose)

            #TODO: might make sense to have this as an attribute since its not changing
            distance_per_step = self.SPEED/(self.model.get_steps_per_hour())

            #If the distance left to reach destination is less than what the UAV
            #will cover in this step, it has reached the destination

            if distance_to_destination > distance_per_step:
                #Haven't reached the destination, keep going...

                #The translation vector
                error_vector = self.model.space.get_heading(self.pos,
                                                            destination_pose)
                #Heading vector is obtained by normalizing (unit vector)
                self.heading = error_vector/ distance_to_destination

                #Compute the new position by adding the translation vector to
                #the old position
                new_position = self.pos + distance_per_step * self.heading
                
                #Add the distance traveled to the odometry
                self._odometer += distance_per_step
                
                #Decrement the fuel available on UAV
                self.fuel -= self.FUEL_CONSUMPTION / (self.model.get_steps_per_hour())
            else:
                #Reached destination!
                new_position = destination_pose  # Set new position to be the destination
                self._odometer += distance_to_destination  # Add actual distance to odometer
                self._reached_destination()


            #Move the agent to the new position
            self.model.space.move_agent(self, new_position)
            self._tfh += 1 / self.model.get_steps_per_hour()
            return

        if self.is_REFUELLING():
            #If uav is refuelling, continue until full
            print("[REFUELLING] UAV {} is at {} refuelling. " \
                  "Current content is {} liters".format(self.unique_id,
                                                        self.source_name,
                                                        self.fuel))
            if self.fuel < self.FUEL_CAPACITY:
                self.fuel += Airport.find_by_name(self.source_name)[0].refuelling_rate
            else:
                self._finished_refuelling()
            return

        if self.is_IDLE():
            #Assumes that loading takes 1 step
            print("[IDLE] UAV {} is at {} idle.".format(self.unique_id,
                                                        self.source_name))