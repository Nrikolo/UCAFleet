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



# =============================================================================
# Fleet
# =============================================================
# A Mesa implementation of an aerial delivery network.
# Uses numpy arrays to represent vectors.
# =============================================================================

import uuid
import random

from mesa import Model
from mesa.space import ContinuousSpace
from schedule import RandomActivationByType

from agents.uav import Uav
from agents.airport import Airport

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
                 steps_per_hour,
                 width=500,
                 height=500):
        '''
        Create a new Fleet model.
        Args:
            airports: a pandas DataFrame with airport name ,  location ,
                probability density function parameters and refuelingRate
                {name, x, y, pdfParams ,refuelingRate, num_uavs}
            steps_per_hour: the number of steps per hour unit of time
            width, height: Size of the space.
        '''
        self._airports = airports
#        self._num_uav_per_airport = num_uav_per_airport
#        self._number_of_uavs = self._num_uav_per_airport * len(airports)
        self._steps_per_hour = steps_per_hour
        self.schedule = RandomActivationByType(self)
        self.space = ContinuousSpace(width, height, False)
        self.parcel_aggregator = list()
        self.make_agents()
        self.running = True

    def get_airport_obj(self, name):
        '''
        returns an airport object based on a name (str)
        '''
        return Airport.find_by_name(name)[0]

    def get_steps_per_hour(self):
        '''
        accessor function to steps per hour of model
        '''
        return self._steps_per_hour

    def get_other_airports(self, airport):
        '''
        accessor function to get other airports than input airport
        '''
        other_airports_indx = self._airports.index.isin([airport.name])
        return self._airports[~other_airports_indx]

    def make_airports(self):
        '''
        Creates airport agents based on the information within the dataframe
        for the airports within the Fleet region of operation (model)
        '''

        #for index, row in df.iterrows():
        #    print row['c1'], row['c2']
        #TODO have a type designation in agents
        for index, row in self._airports.iterrows():
            #print(row)
            #print(row['x'])
            airport = Airport(uuid.uuid4(),
                              self,
                              index,#The airport name
                              (row['x'],row['y']),
                              row['refuelling_rate'] ,
                              row['pdf_params'])
            self.schedule.add(airport)
            self.make_uavs(int(row['num_uavs']), airport) #make a single uav at this airport


    def make_parcels(self):
        '''
        Generate parcels (agents) within airport object

        Contrary to the make_uavs and make_airports methods, the make_parcels
        method gets called every step the model goes through
        '''

        for a in self.schedule.agents_by_type[Airport]:
#            print("in make_parcels, calling airport {}".format(a.name))
            a.generate_parcels()



    def make_uavs(self, amount, airport_obj):
        '''
        Creates an amount of uavs (agents) within airport object
        '''
        #Each airport will have an amount of uavs


        for i in range(amount):
            uav = Uav(uuid.uuid4(), self, airport_obj)
#            uav = Uav(i, self, airportObj)
            airport_obj.store_uav(uav)
            self.space.place_agent(uav, airport_obj.pos)
            self.schedule.add(uav)


    def make_agents(self):
        '''
        Create self.population agents, with airports and uavs
        '''
        self.make_airports()
        self.make_parcels()
        #self.make_uavs() #TODO: decouple airport and UAV creation (TBD)


    def get_random_destination_airport(self, source_name=None):
        '''
        pulls a random airport from the available airports not including
        the source airport name
        '''

        random_airport_name = random.choice(Airport.name_index)
        while random_airport_name == source_name:
            random_airport_name = random.choice(self.name_index)
        return random_airport_name
    

    def step(self):
        # Agent activation should be by this order: airports, packages, uavs
        if not bool (self.schedule.time % self.get_steps_per_hour() ):
            print("---[TIME] Simulation time is {} hours".format(self.schedule.time / self.get_steps_per_hour()))
        self.schedule.step()
        