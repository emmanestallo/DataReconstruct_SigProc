import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

def obtain_packet(): 
    set = []  
    values = np.array(data['Value'])
    for i in range(int(len(data)/16)): 
        set.append(values[16*i:16*(i+1)])
    return set 

def get_DAC(packet): 
    if sum(packet)%2 == 1:
        return 0 
    else: 
        to_dec = packet[1:11] 
        analog = to_dec.dot(2**np.arange(to_dec.size)[::-1])
        dec = analog/1023 
        return dec 

data = pd.read_csv('demod_out_C_Normal_2.txt', sep=" ", header=None)
data.columns = ['Time','Value'] 

data['Value'].replace({-5:0, 5:1}, inplace=True) 
packets = obtain_packet()

analog_values = []
for i in packets: 
    analog_values.append(get_DAC(i)*5) 

time = np.arange(0,len(analog_values)*(1/2000),1/2000)

analog_data = pd.DataFrame({'Time': time, 'Values' : analog_values}) 

analog_data.to_excel('ReconstructedData.xlsx')

sns.set()
sns.set_style("whitegrid") 

plt.plot(time,analog_values)
plt.title('Reconstructed EMG Signal')
plt.xlabel('Time')
plt.ylabel('Voltage (mV)')
plt.show()