
from Orise_Twin_Rotor import Data_Buffers
from Orise_Twin_Rotor import Twin_Rotor
from Orise_Twin_Rotor import Create_Gui,READING_NAMES
import numpy as np

def main():
    twin_rotor = Twin_Rotor()

    data_buffers = Data_Buffers(1000) #creating data buffers to sotre sensor data to be used by the plot -- 1000 data point history will be recorded
    gui_application = Create_Gui(data_buffers) #creating the gui

    gui_application.add_twin_rotor_data("encoder",READING_NAMES.ENCODER1) #adding yaw encoder readings to a plot named encoder
    gui_application.add_time_graph("pitch",lambda x: np.arctan2(x.acc_x.numpy_data,x.acc_z.numpy_data))#type:ignore #displaying the value of atan(accx/accy) in a plot named pitch

    gui_application.start()# starting the application
    
    while True:
        twin_rotor.update_readings() #update the readings -- Must be called otherwise sensor readings will stay the same
        data_buffers.update_buffers(twin_rotor) #update the buffers -- update the buffers that determine plots with the new sensor data
        if not gui_application.active: #if the user closes the gui application this will return False and in such situation terminate the program
            break



if __name__ == "__main__":
    main()
