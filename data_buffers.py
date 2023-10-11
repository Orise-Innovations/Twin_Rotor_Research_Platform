from collections import deque
from twin_rotor import Twin_Rotor
import numpy as np
import threading



class Buffer:
    def __init__(self,size:int):
        self._buffer = deque((0.0 for _ in range(size)))
        self._size = size
    
    def push(self,val:float):
        self._buffer.append(val)
        self._buffer.popleft()

    @property
    def data(self):
        return self._buffer

    @property
    def numpy_data(self):
        return np.array(self._buffer)


class Data_Buffers:
    def __init__(self,size:int):
        self._size = size
        self.time = Buffer(size)
        self.encoder1 = Buffer(size)
        self.encoder2 = Buffer(size)
        self.acc_x = Buffer(size)
        self.acc_y = Buffer(size)
        self.acc_z = Buffer(size)
        self.gyro_x = Buffer(size)
        self.gyro_y = Buffer(size)
        self.gyro_z = Buffer(size)
        self.lock = threading.Lock()

    def update_buffers(self,twin_rotor:Twin_Rotor):
        self.lock.acquire()
        self.time.push(twin_rotor.time_of_last_update)
        self.encoder1.push(twin_rotor.encoder.encoder1)
        self.encoder2.push(twin_rotor.encoder.encoder2)
        self.acc_x.push(twin_rotor.imu.acceleration[0])
        self.acc_y.push(twin_rotor.imu.acceleration[1])
        self.acc_z.push(twin_rotor.imu.acceleration[2])
        self.gyro_x.push(twin_rotor.imu.gyro[0])
        self.gyro_y.push(twin_rotor.imu.gyro[1])
        self.gyro_z.push((twin_rotor.imu.gyro[2]))
        self.lock.release()

    def get_custom_buffer(self):
        return Custom_Buffers(self)

class Custom_Buffers(Buffer):
    def __init__(self,data_buffers:Data_Buffers):
        super().__init__(data_buffers._size)
        self.lock = threading.Lock()

    def push(self,val):
        self.lock.acquire()
        super().push(val)
        self.lock.release()
