# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:00:30 2018

@author: Riko
"""

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout