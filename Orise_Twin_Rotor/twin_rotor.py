import serial
from typing import Callable,Optional

from Orise_Twin_Rotor.encoder import Encoder
from Orise_Twin_Rotor.IMU_lib import IMU
from Orise_Twin_Rotor.motor_driver import Motor
import time

__STANDBY_CODE = b'\x64'
class Twin_Rotor:
    __RUNNING_CODE = b'\x65'
    __ERROR_CODE = b'\x66'
    __STANDBY_CODE = b'\x64'
    def __init__(self,timer_function:Optional[Callable[[],float]] = None):
        '''
        time_function : function used to time updates if None time.monotonic is used
        '''
        self.ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
        self.encoder = Encoder(self.ser)
        self.encoder.wait_until_ready()
        self.imu = IMU()
        self.motors = Motor()

        self._init_time = time.monotonic()
        self.timer_function:Callable[[],float] = self.default_timer_function

        if(timer_function is not None):
            self.timer_function = timer_function

        self._time:float = self.timer_function()
        self.encoder._get_data()
        self.encoder.set_current_to_zero_point()
        self.__set_running()

    def __del__(self):
        self.__set_standby()
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

    def __set_led(self,command):
        self.ser.write(command)

    def __set_running(self):
        self.__set_led(self.__RUNNING_CODE)

    def __set_error(self):
        self.__set_led(self.__ERROR_CODE)

    def __set_standby(self):
        self.__set_led(self.__STANDBY_CODE)

    def show_error(self):
        self.__set_error()
