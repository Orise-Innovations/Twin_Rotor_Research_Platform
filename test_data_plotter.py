
from data_buffers import Data_Buffers
from twin_rotor import Twin_Rotor
from data_plotter import Create_Gui
import numpy as np

def main():
    twin_rotor = Twin_Rotor()

    data_buffers = Data_Buffers(1000)
    gui_application = Create_Gui(data_buffers)
    gui_application.add_time_graph(lambda x: x.encoder1.data)
    gui_application.add_time_graph(lambda x: np.arctan2(x.acc_x.numpy_data,x.acc_z.numpy_data))#type:ignore
    gui_application.start()
    
    while True:
        # print(twin_rotor.update_readings())
        twin_rotor.update_readings()
        data_buffers.update_buffers(twin_rotor)


if __name__ == "__main__":
    main()
