# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:41:37 2018

@author: Riko
"""

from collections import namedtuple

Flight = namedtuple('Flight', ['source_name', 
                               'destination_name',
                               'distance',
                               'duration',
                               'payload',
                               'fuel'])