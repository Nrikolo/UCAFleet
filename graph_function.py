# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 21:48:29 2018

@author: Riko
"""

from agents.parcel import Parcel

import matplotlib.pyplot as plt
def graph_function(model, simulation_time, execution_time):
    
    parcel_age = [p.age / model.get_steps_per_hour() for p in model.schedule.agents_by_type[Parcel]]
    plt.hist(parcel_age)
    plt.title("Parcel Dwell")
    plt.xlabel("Parcel Age [hr]")
    plt.ylabel("Qty []")
    plt.show()
    print("This instance ran for {:.2f}sec simulating {} hours \n" \
          "During which {} parcels were generated, , {:.2f} % ({}) were " \
          "delivered ".format(execution_time,
                              model.schedule.steps / model.get_steps_per_hour(),
                              len(parcel_age),
                              100*len(model.parcel_aggregator) / len(parcel_age),
                              len(model.parcel_aggregator)))
    
    from agents.uav import Uav
    TFH = [u._tfh for u in model.schedule.agents_by_type[Uav]]
    utilization = [x / simulation_time*100 for x in TFH]
    plt.hist(utilization)
    plt.title("UAV Utilization")
    plt.xlabel("Percent Utilization of UAV [%]")
    plt.ylabel("Qty []")
    print("The graph above is a uav utilization histogram")
    
    plt.show()
    
    
