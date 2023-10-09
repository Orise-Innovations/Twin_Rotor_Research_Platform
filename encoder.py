from typing import Tuple,Optional
from serial import Serial
import struct
from time import sleep
class Encoder:
    COMMAND_BYTE = b'\x63' 
    DATA_SIZE =8 

    def __init__(self,ser:Serial) -> None:
        self._ser = ser
        self._encoder_1 = 0
        self._encoder_2 = 0
        self._zero_point_1 = 0
        self._zero_point_2 = 0
    def wait_until_ready(self):
        '''
        Blocks untli the system is ready
        '''
        while True:
            data = self._get_data()
            if(data is not None):
                break
            print("STM32 Not Ready yet")
            sleep(1)

    def set_zero_point(self,zero_point1,zero_point2):
        self._zero_point_1 = zero_point1
        self._zero_point_2 = zero_point2

    def set_current_to_zero_point(self):
        self._zero_point_1,self.zero_point_2 = self._encoder_1,self._encoder_2
    def _get_data(self)->Optional[Tuple[int,int]]:
        '''
        queries the encoders and gets the data returns a tuple of ints 
        if unable to aquire within the timeout specified in the serial timeout
        returns None
        '''
        if(self._ser.in_waiting):
            self._ser.flushInput()#type:ignore
        self._ser.write(self.COMMAND_BYTE)#type:ignore
        # sleep(0.01)
        # assert(self._ser.in_waiting == 8)
        read_val = self._ser.read(self.DATA_SIZE)
        if(len(read_val)!=8):
            return None
        return struct.unpack('<ii',read_val)#type:ignore

    @property
    def encoder1(self):
        '''
        value of encoder1 after last update
        '''
        return self._encoder_1 - self._zero_point_1

    @property
    def encoder2(self):
        '''
        value of encoder1 after last update
        '''
        return self._encoder_2 - self._zero_point_2
    
    def update(self):
        '''
        updates the internally stored encoder values
        if unable to obtain the data the values won't be updated and returns False
        otherwise returns False
        '''
        data = self._get_data()
        if(data is None):
            return False
        self._encoder_1,self._encoder_2 =data
        return True

    def __str__(self):
        return f"Encoder1={self.encoder1} Encoder2={self.encoder2}"
    
    def __repr__(self):
        return self.__str__()








        


    