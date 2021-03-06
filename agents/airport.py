# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:49:52 2018

@author: Riko
"""
import logging
from collections import deque, defaultdict

import numpy as np

from mesa import Agent

from agents.parcelqueue import ParcelQueue


class Airport(Agent):
    '''
    A Airport agent with the following attributes:
        NAME (string)
        Package Queues {one for each of the other airports} #those within range???
        Package PDF (probability density function)
        UAV Queue (FIFO queue) of UAV agents in that airport
        pos (x,y) in km
        REFUELING_RATE in Liters/step
        Package storage
    '''
    name_index = defaultdict(list)

    def __init__(self, unique_id, model, name, pos, refuelling_rate, pdf):
        '''
        Create a airport agent.
        Args:
            unique_id: UUID
            model:
            name:
            pos:
            refulling_rate:
            pdf:
        '''
        logging.info("[SPAWN] Creating an airport instance with id %s in %s",
                     unique_id,
                     name)
        super().__init__(unique_id, model)
        self.type_ = 'airport'
        self.name = name
        self.pos = np.array(pos)
        self.refuelling_rate = refuelling_rate
        self.pdf = pdf
        self.uav_queue = deque()  # An empty queue for UAVs
        self.parcel_storage_queue = deque()  # An empty queue for storage of incoming parcels
        self.parcel_queues = list()
        # Create a parcel queue for each of the OTHER airports in the model
        # Assumes all airports are within range and a single flight is required to deliver a parcel
        for index, _ in self.model.get_all_airports().iterrows():
            if index == self.name:  # Airport from the list is the same as being constructed
                continue
            self.parcel_queues.append(ParcelQueue(self.model,
                                                  self.name,
                                                  index))  # Create a parcel queue
        Airport.name_index[self.name].append(self)
#        print("")
#        print(Airport.name_index)

    @classmethod
    def find_by_name(cls, name):
        '''
        enables query by name at the class level
        '''
        return Airport.name_index[name]

# =============================================================================
#     pseudo private methods
# =============================================================================

    def _load_uav(self, uav_obj):
        '''
        Attempts to load a uav
        If there are more than MIN_PAYLOAD packages for one destination
        function will load (for now return) a list of packages
        '''
        # TODO: Can more than one UAV be loaded per step?
        for qu in self.parcel_queues:
#            print("Parcel queue destination is {}".format(q.destination_name))
            #iterate throught the queue of parcels for a specific destination
            shipment_size, shipment_mass = qu.get_shipment(uav_obj.MIN_PAYLOAD,
                                                           uav_obj.MAX_PAYLOAD)
#            print("Trying to load {} parcels in _load_uav stationed in {}".format(shipment_size,
#                                                                                  self.name))
            if shipment_size:
                uav_obj.load(qu.remove_parcels(shipment_size),
                             qu.destination_name,
                             shipment_mass)
            if uav_obj.is_loaded():
#                print("UAV {} is loaded with {} parcels totaling {} kg ".format(uav_obj.unique_id,
#                                                                                shipment_size,
#                                                                                shipment_mass))
                return True
            else:
                continue #  Continue to the next queue in the airport
            #No UAV was loaded
            return False

    def _unload_uav(self, uav_obj):
        '''
        Attempts to unload a uav

        Gets the parcels, sets their age and puts them all into airport storage
        while removing them from the uav
        '''

        logging.info("[UNLOADING] UAV {} in _unload_uav stationed in {}".format(uav_obj.unique_id,
                                                                               self.name))

        shipment = uav_obj.get_parcels()
        # Set the parcels life span
        for parcel in shipment:
            parcel.delivered()

        # Store the incoming parcels to the airport storage queue
        self.parcel_storage_queue += shipment

        #Move them to model "aggragator"
        self.model.parcel_aggregator += shipment

        # Unload the uav
        uav_obj.unload()

    def _sort_parcel_queues(self, priority=None):
        '''
        sorts the airport's parcel queues based on criteria
        '''

        #TODO: decide on the order of priority to loop though the parcel queues
        # in the airport. it would make sense that self.parcel_queues is sorted based on
        # the criteria
        # Consider implementing one or all
        # --The q with the most packages (Priority = amount)
        #https://stackoverflow.com/questions/30346356/how-to-sort-list-of-lists-according-to-length-of-sublists
        # --The q with the oldest package (Priority = oldest)
        # --The q with the highest average age (Priority = oldest_avg)
        pass

# =============================================================================
# pseudo public methods
# =============================================================================

    def generate_parcels(self, number=1):
        '''
        generates parcels in the airport based on probability density function
        '''
        #TODO: use pdf_parameters
#        print("Airport {} is generating parcels".format(self.name))
#        print("Airport has these queues {}".format(self.parcel_queues))
        # Iterate through all parcel queue objects and generate parcels
        for qu in self.parcel_queues:
            qu.generate_parcels(number)

    def release_uav(self, uav_obj):
        '''
        removes uav object set to takeoff from the airport's uav_queue
        and returns True if succesful and false if this uav isn't in the airport queue
        '''
        if uav_obj in self.uav_queue:
            logging.info("[RELEASE] %s airport is removing uav %s",
                         self.name,
                         uav_obj.unique_id)
            self.uav_queue.remove(uav_obj)
            return True
        else:
            return False

    def get_queues_as_dict(self):
        '''
        functions converts the parcel queue within an airport to a dict
        '''
        queue_dict = {}
        for i in self.parcel_queues:
            queue_dict[i.destination_name] = (i.get_size(),
                                              round(i.get_avg_age() / self.model.get_steps_per_hour(), 1),
                                              round(i.get_max_age() / self.model.get_steps_per_hour(), 1))
        return queue_dict

    def get_number_parcels(self):
        '''
        returns the total number of parcels meant to be shipped out of this airport now
        '''
        return sum(q.get_size() for q in self.parcel_queues)


    def store_uav(self, uav_obj):
        '''
        recieve a uav object and store it in the airport's FIFO queue
        '''
        logging.info("[STORE] %s airport is queueing uav %s",
                     self.name,
                     uav_obj.unique_id)

        self.uav_queue.append(uav_obj)


    def step(self):
        '''
        A step in the airports timeline.

        Sorting parcels, Generating parcels,Refuling UAVs, Loading UAVs, Unloading UAVs
        '''
        # TODO: Change so that only one loading and sending a UAV can happen in a single step
        # (generalize and convert to time window, i.e takeoff possible every T minutes
#        print("In airport {} step function".format(self.name))
        self._sort_parcel_queues()  # Prioritize the parcel queues
        self.generate_parcels()  # Creating parcels at this airport

        # Try and load IDLE uavs and unload refueling loaded uavs
        for uav_obj in list(self.uav_queue): # Loop through the UAV Queue (FIFO)
#            print("UAV {} is in state {} ".format(uav_obj.unique_id,
#                                                  uav_obj.get_state()))
            if uav_obj.is_idle() and (not uav_obj.is_loaded()): #verify it is idle and ready to load
#                print("Attempting to load UAV {}".format(uav_obj.unique_id))
                #Try and load it
                if self._load_uav(uav_obj):
                    logging.info("[LOADED] UAV %s was loaded succesfully at %s" \
                                 "with %3d parcels totalling %.2f kg ",
                                 uav_obj.unique_id,
                                 self.name,
                                 len(uav_obj.get_parcels()),
                                 uav_obj.get_payload_mass())
            elif (uav_obj.is_refuelling() and uav_obj.is_loaded()):
#                print("Attempting to unload {}".format(uav_obj.unique_id))
                self._unload_uav(uav_obj)
                logging.info("[UNLOADED] UAV %s was unloaded succesfully at %s",
                             uav_obj.unique_id,
                             self.name)
            elif (uav_obj.is_refuelling() and not uav_obj.is_loaded()):
                pass # uav is refuelling, will increment fuel during its step method
            continue
