# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:49:52 2018

@author: Riko
"""

import numpy as np

from mesa import Agent


class Airport(Agent):
    '''
    A Airport agent with the following attributes:
        NAME (string)
        Package Queues {one for each of the other airports}
        Package PDF (probability density function)
        UAV Queue (list) of UAV agents in that airport
        POSITION (x,y) in km
        REFUELING_SPEED in Liters/step 
  

    '''
    def __init__(self, unique_id, model, pos):
        '''
        Create a airport agent.
        Args:
            speed: Distance to move per step.

        '''
        super().__init__(unique_id, model)
        self._position = np.array(pos)
        
     
