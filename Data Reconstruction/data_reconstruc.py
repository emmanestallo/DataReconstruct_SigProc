import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

#separates the digital data to packets with length 16 bits 
def obtain_packet(items): 
    set = []  
    values = np.array(items['Value'])
    for i in range(int(len(items)/16)): 
        set.append(values[16*i:16*(i+1)])
    return set 

#processes the obtained packets for digital to analog conversion 
def get_DAC(packet): 
    if sum(packet)%2 == 1:
        return 0 
    else: 
        to_dec = packet[1:11] 
        analog = to_dec.dot(2**np.arange(to_dec.size)[::-1])
        dec = analog/1023 
        return dec 

#obtains the time vector and the analog data
def get_time_value(df):
    df['Value'].replace({-5:0, 5:1}, inplace=True)
    packets = obtain_packet(df)
    analog_values = [] 
    for i in packets: 
        analog_values.append(get_DAC(i)*5) 
    time = np.arange(0,len(analog_values)*(1/2000),1/2000)
    return time, analog_values

#export to xlsx
def export_xlsx(x,y,title):
    analog_data = pd.DataFrame({'Time': x, 'Values' : y}) 
    analog_data.to_excel(f'{title}.xlsx')

data_1 = pd.read_csv('demod_out_A_Normal_2.txt', sep=" ", header=None)
data_1.columns = ['Time','Value']

data_2 = pd.read_csv('demod_out_C_Normal_2.txt', sep=" ", header=None)
data_2.columns = ['Time','Value'] 

data_3 = pd.read_csv('demod_out_B_BPI_2.txt', sep=" ", header=None)
data_3.columns = ['Time','Value'] 

time_1,analog_values_1 = get_time_value(data_1)
time_2,analog_values_2 = get_time_value(data_2)
time_3,analog_values_3 = get_time_value(data_3)

export_xlsx(time_1, analog_values_1,'demod_out_A_normal_2')
export_xlsx(time_2, analog_values_2,'demod_out_C_normal_2')
export_xlsx(time_3, analog_values_3,'demod_out_B_BPI_2')

#plotting 
sns.set()
sns.set_style("whitegrid") 

fig,axes = plt.subplots(2)
axes[0].plot(time_1,analog_values_1) 
axes[1].plot(time_2,analog_values_2)

axes[0].set_title('demod_out_A_Normal_2')
axes[1].set_title('demod_out_C_Normal_2')

axes[0].set_ylabel('Voltage (mV)')
axes[0].set_xlabel('Time (s)')

axes[1].set_ylabel('Voltage (mV)')
axes[1].set_xlabel('Time (s)')

plt.tight_layout()
plt.show()