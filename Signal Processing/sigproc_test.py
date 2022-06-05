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
b10Hz, a10Hz = sigproc.butter(4,fc1,'high', analog=False, fs=2000) 
#b450Hz, a450Hz = sigproc.butter(4,fc2,'low', analog=False, fs= 2000) 
b20Hz, a20Hz = sigproc.butter(2,fc3,'low', analog=False, fs=2000)

#filter and envelope detector
sig1 = sigproc.filtfilt(b10Hz,a10Hz,val) 
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

min_SD_idx = np.argmin(np.min(SD))
mean_min_idx = mean[min_SD_idx]  

h=5

th = mean_min_idx + h*np.min(SD)

onset_time = [] 
offset_time = []

for idx in range (len(sig_filt)): 
    if (sig_filt[idx] > th) and (len(onset_time) == len(offset_time)): 
        onset = True 
        for element in sig_filt[idx:idx+25]:
            if element < th: 
                onset = False 
        if onset:
            onset_time.append(time[idx]) 

    elif (sig_filt[idx] < th) and (len(onset_time) > len(offset_time)): 
        offset = True
        for element in sig_filt[idx:idx+25]:
            if element > th: 
                offset = False 
        if offset:
            offset_time.append(time[idx])


print(onset_time)
print(offset_time)
sns.set()
sns.set_style("darkgrid")
plt.plot(time,sig_filt)
plt.show()