from simple_pid import PID
from twin_rotor import Twin_Rotor
from time import sleep

MAX_SPEED = 600*5
Kp = MAX_SPEED//2
Kd = 0
Ki = 0
Limits = (-MAX_SPEED//2,MAX_SPEED//2)
constant = MAX_SPEED//2
class Stable_Contoller:
    def __init__(self):
        self.twin_rotor = Twin_Rotor()
        self.pid = PID(Kp,Ki,Kd,0,output_limits=Limits)

    def __del__(self):
        self.twin_rotor.stop()

    def set_set_point(self,point):
        self.pid.setpoint = point

    def run(self):
        self.twin_rotor.update_readings()
        angle = self.twin_rotor.imu.simple_pitch_from_g_fusion
        val = self.pid(angle)
        print(val)
        if(val is not None):
            self.twin_rotor.motors.set_speed(constant+val,-constant+val)
        else:
            print("PID fail?")
        return val
    
    



def main():
    controller = Stable_Contoller()
    while True:
        controller.run()
        sleep(0.001)

if __name__ == "__main__":
    main()