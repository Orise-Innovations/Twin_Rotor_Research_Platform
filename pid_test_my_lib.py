from pid_lib import PID
from twin_rotor import Twin_Rotor
from time import sleep
from data_buffers import Data_Buffers
from data_plotter import Create_Gui,Colors
from data_logger import CSV_Logger
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
    
    



def main():
    FILE_PATH =  "logging_test/csv_data_logger_57.csv"
    data_logger = CSV_Logger(FILE_PATH)
    controller = Stable_Contoller()
    controller.set_set_point(radians(30))
    data_buffers = Data_Buffers(1000)
    gui_application = Create_Gui(data_buffers)
    gui_application.add_time_graph(lambda x: x.encoder1.data,"encoder1")
    gui_application.add_time_graph(lambda x: np.arctan2(x.acc_x.numpy_data,x.acc_z.numpy_data),"pitch",Colors.ORISE_ORANGE)#type:ignore
    gui_application.start()
    while True:
        data_buffers.update_buffers(controller.twin_rotor)
        controller.run()
        data_logger.log(controller.twin_rotor)
        sleep(0.001)

if __name__ == "__main__":
    main()