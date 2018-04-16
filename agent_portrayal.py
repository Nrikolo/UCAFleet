# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:14:05 2018

@author: Riko
"""
from agents.uav import Uav
from agents.airport import Airport
from agents.parcel import Parcel

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Airport:
        print(agent)
        return {"Shape": "circle",
                "r": 4,
                "Filled": "true",
                "Color": "#00FF00",
                "Layer": 1,
                "text": agent.name,
                "text_color": "black"}
    elif type(agent) is Uav:        
        return {"Shape": "circle",
                "r": 2,
                "Filled": "true",
                "Color": "Red",
                "Layer": 2,
                "text": round(agent.fuel, 1),
                "text_color": "black"}
    elif type(agent) is Parcel:
        pass

    return portrayal

#https://github.com/projectmesa/mesa/blob/master/examples/wolf_sheep/wolf_sheep/server.py

#    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}
#         return {"Shape": "arrowHead",
#                "Filled": "true",
#                "Layer": 2,
#                "Color": ["#00FF00", "#99FF99"],
#                "stroke_color": "#666666",
#                "Filled": "true",
#                "heading_x": agent.heading[0],
#                "heading_y": agent.heading[1],
#                "text": agent.unique_id,
#                "text_color": "black",
#                "scale": 0.8}

#https://github.com/projectmesa/mesa/blob/ea390b7f52bf77edb484255b24bd2973e64fbd4d/mesa/visualization/templates/js/GridDraw.js


