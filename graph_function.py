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
    plt.show()
    print("This simulation was running for {} hours and ran for {:.2f}sec \n" \
          "During which {} parcels were generated, {} were " \
          "delivered, {:.2f} % ".format(model.schedule.steps / model.get_steps_per_hour(),
                                        execution_time,
                                        len(parcel_age),
                                        len(model.parcel_aggregator),
                                        100*len(model.parcel_aggregator) / len(parcel_age)))
    
    from agents.uav import Uav
    TFH = [u._tfh for u in model.schedule.agents_by_type[Uav]]
    utilization = [x / simulation_time*100 for x in TFH]
    plt.hist(utilization)
    plt.show()
    
    
