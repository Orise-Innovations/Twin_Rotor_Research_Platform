from motor_driver import Motor
from encoder import Encoder
from simple_pid import PID
from IMU_lib import IMU
import serial

MAX_SPEED = 600*5
Kp = MAX_SPEED//2
Kd = 0
Ki = 0
Limits = (-MAX_SPEED//2,MAX_SPEED//2)
constant = MAX_SPEED//2
class Stable_Contoller:
    def __init__(self,ser):
        self.encoder = Encoder(ser)
        self.motor = Motor()
        self.pid = PID(Kp,Ki,Kd,0,output_limits=Limits)
        self.imu = IMU()

    def __del__(self):
        self.stop()
    def set_set_point(self,point):
        self.pid.setpoint = point
    def run(self):

        angle = self.imu.simple_pitch_from_g_fusion
        val = self.pid(angle)
        print(val)
        if(val is not None):
            self.motor.set_speed_M0(constant+val)
            self.motor.set_speed_M1(-constant+val)
        else:
            print("PID fail?")
        return val
    
    def stop(self):
        self.motor.stopM0()
        self.motor.stopM1()
    



def main():
    ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
    controller = Stable_Contoller(ser)
    while True:
        controller.run()

if __name__ == "__main__":
    main()