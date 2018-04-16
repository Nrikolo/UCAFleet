# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:46:44 2018

@author: Riko
"""

#server.py

from mesa.visualization.ModularVisualization import ModularServer
from SimpleContinuousModule import SimpleCanvas

from model import Fleet

from agent_portrayal import agent_portrayal 

from input_data import airports, steps_per_hour

width = airports['x'].max() + 20.
height = airports['y'].max() + 20.

fleet_canvas = SimpleCanvas(agent_portrayal, width, height)

model_params = {"airports": airports,
                "steps_per_hour": steps_per_hour,
                "width": width,
                "height": height}

server = ModularServer(Fleet, [fleet_canvas], "Fleet Simulation", model_params)