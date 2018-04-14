# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:00:30 2018

@author: Riko
"""

import sys, os 


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    