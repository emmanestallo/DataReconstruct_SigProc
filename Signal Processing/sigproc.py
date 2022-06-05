import numpy as np 
from scipy import signal as sigproc 
import pandas as pd 
import matplotlib.pyplot as plt 


fc1 = 10 
fc2 = 450 
fc3 = 20 

butterHP_10Hz = sigproc.butter(4,10,'high', analog=False, fs=2000) 
butterENVLP_450Hz = sigproc.butter(4,450,'low', analog=False, fs= 2000) 
butterENVHP_20Hz = sigproc.butter(2,20,'high', analog=False, fs=2000)

