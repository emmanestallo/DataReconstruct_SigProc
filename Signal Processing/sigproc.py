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

b10Hz, a10Hz = sigproc.butter(4,10,'high', analog=False, fs=2000) 
b450Hz, a450Hz = sigproc.butter(4,450,'low', analog=False, fs= 2000) 
b20Hz, a20Hz = sigproc.butter(2,20,'high', analog=False, fs=2000)

sig1 = sigproc.filtfilt(b10Hz,a10Hz, val) 
sig2 = sigproc.filtfilt(b450Hz,a450Hz, sig1) 
sig_filt = sigproc.filtfilt(b20Hz,a20Hz,sig2) 

rs = np.abs(sig_filt) 

window = 0.3 
period = 1/2000 
SD = []

nsamp = int(window/period)
pad = np.zeros(430) 

zero_pad_val = np.append(val,pad)

sets = [zero_pad_val[n:n+nsamp] for n in range(0,len(val),nsamp)]

SD = [np.std(element) for element in sets]

print(SD)

sns.set()
sns.set_style("darkgrid")
plt.plot(time,rs)
plt.show()