#filter designer 
from scipy import signal as sigproc 
import matplotlib.pyplot as plt  
import numpy as np 


fc1 = 10 
fc3 = 20 

b10Hz, a10Hz = sigproc.butter(4,fc1,'high', analog=False, fs=2000) 
b20Hz, a20Hz = sigproc.butter(2,fc3,'low', analog=False, fs=2000)

angle, freq_resp = sigproc.freqz(b20Hz, a20Hz, whole = False) 

plt.plot(angle, 20*np.log10(abs(freq_resp)), color = 'b')
plt.show()
