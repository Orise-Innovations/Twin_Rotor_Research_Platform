import matplotlib.pyplot as plt
from Orise_Twin_Rotor.matplotlib_plotter import Matplotlib_Plotter

from Orise_Twin_Rotor import Twin_Rotor
from Orise_Twin_Rotor import Data_Buffers
import threading
from typing import Iterable
import numpy as np
from time import time
import matplotlib

# Create figure for plotting
twin_rotor = Twin_Rotor()
data_buffers = Data_Buffers(1000)
m = Matplotlib_Plotter(data_buffers,(2,2))

def plot_angle(buffer_data:Data_Buffers)->Iterable[float]:
    acc_x = buffer_data.acc_x.numpy_data
    acc_y = buffer_data.acc_y.numpy_data
    return np.arctan(acc_x,acc_y)#type:ignore
    
m.add_time_plot(lambda x : x.encoder1.data,"encoder1",0,0)
m.add_time_plot(plot_angle,"acc_pitch",0,1)
m.add_time_plot(lambda x: x.gyro_x.data ,"gyro_x",1,0)
m.add_time_plot(lambda x: x.gyro_y.data ,"gyro_y",1,1)
while True:
    twin_rotor.update_readings()
    data_buffers.update_buffers(twin_rotor)
    m.draw()

    