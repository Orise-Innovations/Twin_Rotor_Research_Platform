from typing import Tuple,Optional
from serial import Serial
import struct
from time import sleep
COMMAND_BYTE = b'\x63' 
DATA_SIZE =8 
class Encoder:

    def __init__(self,ser:Serial) -> None:
        self._ser = ser
    def wait_until_ready(self):
        while True:
            data = self.get_data()
            if(data is not None):
                break
            print("STM32 Not Ready yet")
            sleep(1)

    def get_data(self)->Optional[Tuple[int,int]]:
        if(self._ser.in_waiting):
            self._ser.flushInput()#type:ignore
        self._ser.write(COMMAND_BYTE)#type:ignore
        # sleep(0.01)
        # assert(self._ser.in_waiting == 8)
        read_val = self._ser.read(DATA_SIZE)
        if(len(read_val)!=8):
            return None
        return struct.unpack('<ii',read_val)#type:ignore






        


    