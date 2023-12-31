from Orise_Twin_Rotor import PID
from Orise_Twin_Rotor import Twin_Rotor
from time import sleep
from Orise_Twin_Rotor import Data_Buffers
from Orise_Twin_Rotor import Create_Gui,READING_NAMES
from Orise_Twin_Rotor import CSV_Logger
import numpy as np
from math import radians


MAX_SPEED = 600*6
Kp = 0.342
Kd = 0.222
Ki = 0.132
Limits = (-MAX_SPEED//2,MAX_SPEED//2)
constant =  MAX_SPEED//2
class Stable_Contoller:
    def __init__(self):
        self.twin_rotor = Twin_Rotor()
        self.pid = PID(Kp,Ki,Kd,Limits,derivative_filter_omega=5,derivative_on_measurement=False)
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
    
    



def main():
    FILE_PATH =  "logging_test/csv_data_logger.csv"
    data_logger = CSV_Logger(FILE_PATH)
    controller = Stable_Contoller()
    controller.set_set_point(radians(30))
    data_buffers = Data_Buffers(1000)
    gui_application = Create_Gui(data_buffers)
    gui_application.add_twin_rotor_data("encoder",READING_NAMES.ENCODER1)
    gui_application.add_time_graph("pitch",lambda x: np.arctan2(x.acc_x.numpy_data,x.acc_z.numpy_data),color=(255,0,255))#type:ignore
    gui_application.start()
    while True:
        data_buffers.update_buffers(controller.twin_rotor)
        controller.run()
        data_logger.log(controller.twin_rotor)
        sleep(0.001)
        if not gui_application.active:
            break

if __name__ == "__main__":
    main()
