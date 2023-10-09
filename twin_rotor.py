import serial
from typing import Callable,Optional

from encoder import Encoder
from IMU_lib import IMU
from motor_driver import Motor
import time

class Twin_Rotor:
    def __init__(self,timer_function:Optional[Callable[[],float]] = None):
        '''
        time_function : function used to time updates if None time.monotonic is used
        '''
        self.ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
        self.encoder = Encoder(self.ser)
        self.imu = IMU()
        self.motors = Motor()

        self._init_time = time.monotonic()
        self.timer_function:Callable[[],float] = self.default_timer_function

        if(timer_function is not None):
            self.timer_function = timer_function

        self._time:float = self.timer_function()

    def __del__(self):
        self.ser.close()

    def default_timer_function(self)->float:
        return time.monotonic() - self._init_time

    def stop(self):
        self.motors.stop()

    def update_readings(self)->float:
        '''
        updates the readings for imu and encoder and sets the update time
        returns the time delta 
        '''
        self.imu.update()
        self.encoder.update()
        ct = self.timer_function()
        pt = self._time
        self._time = ct
        return (ct-pt)

    @property
    def time_of_last_update(self):
        return self._time

    def __str__(self):
        return f"t={self.time_of_last_update} {self.encoder} {self.imu}"

