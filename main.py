from motor_driver import Motor
from encoder import Encoder
from simple_pid import PID
import serial

Kp = 0
Kd = 0
MAX_SPEED = 10_000
Ki = 0
Limits = (-MAX_SPEED,MAX_SPEED)
constant = 10_000
class Stable_Contoller:
    def __init__(self,ser):
        self.encoder = Encoder(ser)
        self.motor = Motor()
        self.pid = PID(Kp,Ki,Kd,0,output_limits=Limits)

    def __del__(self):
        self.stop()
    def set_set_point(self,point):
        self.pid.setpoint = point
    def run(self):
        data= self.encoder.get_data()
        if(data is None):
            return
        encoder1,encoder2 =data
        val = self.pid(encoder1)
        if(val is not None):
            self.motor.speedControlM0(constant+val)
            self.motor.speedControlM1(constant-val)
        else:
            print("PID fail?")
    
    def stop(self):
        self.motor.stopM0()
        self.motor.stopM1()
    



def main():
    ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
    controller = Stable_Contoller(ser)
    while True:
        controller.run()