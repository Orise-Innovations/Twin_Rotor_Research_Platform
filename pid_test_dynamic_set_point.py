from Orise_Twin_Rotor import PID
from Orise_Twin_Rotor import Twin_Rotor
from time import sleep
from Orise_Twin_Rotor import Data_Buffers
from Orise_Twin_Rotor import Create_Gui,READING_NAMES
from Orise_Twin_Rotor import CSV_Logger
import numpy as np
import math
from time import time

MAX_SPEED = 600*6
Kp = 0.342
Kd = 0.222
Ki = 0.132


## NEw VALUES FOR DYNAMIC SYSTEM######
Ki = 0.6
Kd = 0.5
######################################

Limits = (-MAX_SPEED//2,MAX_SPEED//2)
constant =  MAX_SPEED//2
class Stable_Contoller:
    def __init__(self):
        self.twin_rotor = Twin_Rotor()
        self.pid = PID(Kp,Ki,Kd,Limits,derivative_filter_omega=5,derivative_on_measurement=True)
        self.angle = 0
        self.beta = 0.5

    def __del__(self):
        self.twin_rotor.stop()

    def set_set_point(self,point):
        self.pid.set_set_point(point)

    def run(self):
        time_delta = self.twin_rotor.update_readings()
        angle = self.twin_rotor.imu.simple_pitch_from_g_fusion
        # self.angle = angle*(self.beta)+self.angle*(1-self.beta)
        val = MAX_SPEED/2*self.pid(angle,time_delta)

        self.twin_rotor.motors.set_speed(constant+val,-constant+val)
        return val
    
    

def dynamic_set_point_sin(t):
    f = 0.1
    return math.radians(30)*math.sin(2*math.pi*f*t) 

def dynamic_set_point_square(t):
    f = 0.05
    return (t % (1/f) > (1/f/2))*math.radians(30)


def main():
    FILE_PATH =  "logging_test/csv_data_logger_57.csv"
    data_logger = CSV_Logger(FILE_PATH)
    controller = Stable_Contoller()
    controller.set_set_point(0)
    data_buffers = Data_Buffers(1000)
    custom_buffers = data_buffers.get_custom_buffer()
    gui_application = Create_Gui(data_buffers)
    gui_application.add_time_graph("encoder1",lambda x: x.encoder1.data)
    gui_application.add_twin_rotor_data("mag",READING_NAMES.MAG_X,(255,0,0),"mag_x")
    gui_application.add_twin_rotor_data("mag",READING_NAMES.MAG_Y,(0,255,0),"mag_y")
    gui_application.add_twin_rotor_data("mag",READING_NAMES.MAG_Z,(0,0,255),"mag_z")
    gui_application.add_time_graph("pitch",lambda x: np.arctan2(x.acc_x.numpy_data,x.acc_z.numpy_data),(0,255,255),"actual")#type:ignore
    gui_application.add_custom_buffer_graph("pitch",custom_buffers,(0,255,0),"set_point")
    gui_application.start()
    t = time()
    while True:
        data_buffers.update_buffers(controller.twin_rotor)
        controller.run()
        data_logger.log(controller.twin_rotor)
        point = dynamic_set_point_square(time()-t)
        custom_buffers.push(point)
        controller.set_set_point(point)
        sleep(0.001)

if __name__ == "__main__":
    main()