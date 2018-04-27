# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:14:05 2018

@author: Riko
"""
from agents.uav import Uav
from agents.airport import Airport
from agents.parcel import Parcel

import json

def convert(list_of_queues): 
    '''
    functions converts the parcel queue within an airport to a dict and then to json
    '''
    d = {}
    for i in list_of_queues: 
        d[i.destination_name] = (i.get_size(),  round(i.get_avg_age(),1))
#        print("[CONVERT] converting in airport {} to json from {} with {} parcels:".format(i.source_name, i.destination_name, i.get_size()))
#    print ("---------------")    
    return json.dumps(d)
    
#convert(agent.parcel_queues)
    
def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Airport:
        return {"Shape": "airport",
                "r": 4,
                "Filled": "true",
                "Color": "#00FF00",
                "Layer": 0,
                "name": agent.name,
                "queues": json.dumps(agent.get_queues_as_dict()),
                "text_color": "black"}
    elif type(agent) is Uav:        
        return {"Shape": "uav",
                "r": 2,
                "Filled": "true",
                "Color": "Red",
                "Layer": 2,
                "name": agent.unique_id.hex[-5:], #present only the last 5 bytes
                "fuel": round(agent.fuel, 1),
                "payload_mass":round(agent.get_payload_mass(),1), 
                "payload_qty":agent.get_payload_qty(), 
                "src": agent.source_name,
                "dest": agent.destination_name,
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


