import os
import sys


import configparser
from simulation.exeution import MonteCarlo

# model import 
from model.resilience.model import ResistanceModel 
from model.windLoad.model import WindLoadModel



if __name__ == "__main__":
    
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    
    # model load ---------------------—
    r = ResistanceModel(config)
    w = WindLoadModel(config)
    f = None #ベット作成予定
    
    # simulation load -----------------
    mc = MonteCarlo(r,w,f=None)
    mc.loop_pi()