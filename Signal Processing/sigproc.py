import numpy as np 
from scipy import signal as sigproc 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

data = pd.read_csv('demod_out_A_normal_2.csv')

time = data['Time'].to_numpy()
val = data['Values'].to_numpy()

fc1 = 10 
fc2 = 450 
fc3 = 20 

#filter parameters
b10Hz, a10Hz = sigproc.butter(4,10,'high', analog=False, fs=2000) 
#b450Hz, a450Hz = sigproc.butter(4,450,'low', analog=False, fs= 2000) 
b20Hz, a20Hz = sigproc.butter(2,20,'low', analog=False, fs=2000)

#filter and envelope detector
sig1 = sigproc.filtfilt(b10Hz,a10Hz, val) 
rs = np.abs(sig1)
#sig2 = sigproc.filtfilt(b450Hz,a450Hz, sig1) 

#post-processed signal
sig_filt = sigproc.filtfilt(b20Hz,a20Hz,rs) 


window = 0.3 
period = 1/2000 
SD = []

nsamp = int(window/period)

sets = [sig_filt[n:n+nsamp] for n in range(0,len(sig_filt),nsamp)]

SD = np.array([np.std(element) for element in sets])
mean = np.array([np.mean(element) for element in sets])

min_SD_idx = np.where(SD == np.min(SD))
mean_min_idx = mean[min_SD_idx]  

h=3

th = mean_min_idx + h*np.min(SD) 

onset = [] 
offset = []

for idx in range(len(val)-25):
    decision = []
    to_comp = val[idx:idx+25]
    for elem in to_comp: 
        if elem < th: 
            decision.append(False) 
        else:
            decision.append(True) 
    if all(decision):
        onset.append(val[idx])

for idx in range(len(val)-25):
    decision = []
    to_comp = val[idx:idx+25]
    for elem in to_comp: 
        if elem > th: 
            decision.append(False) 
        else:
            decision.append(True) 
    if all(decision):
        offset.append(val[idx])

print(th)
            

print(len(onset)) 
print(len(offset))
        

sns.set()
sns.set_style("darkgrid")
plt.plot(time,sig_filt)
plt.show()