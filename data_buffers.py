from collections import deque
from twin_rotor import Twin_Rotor

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

class Data_Buffers:
    def __init__(self,size:int):
        self.time = Buffer(size)
        self.encoder1 = Buffer(size)
        self.encoder2 = Buffer(size)
        self.acc_x = Buffer(size)
        self.acc_y = Buffer(size)
        self.acc_z = Buffer(size)
        self.gyro_x = Buffer(size)
        self.gyro_y = Buffer(size)
        self.gyro_z = Buffer(size)

    def update_buffers(self,twin_rotor:Twin_Rotor):
        self.time.push(twin_rotor.time_of_last_update)
        self.encoder1.push(twin_rotor.encoder.encoder1)
        self.encoder2.push(twin_rotor.encoder.encoder2)
        self.acc_x.push(twin_rotor.imu.acceleration[0])
        self.acc_y.push(twin_rotor.imu.acceleration[1])
        self.acc_z.push(twin_rotor.imu.acceleration[2])
        self.gyro_x.push(twin_rotor.imu.gyro[0])
        self.gyro_y.push(twin_rotor.imu.gyro[1])
        self.gyro_z.push((twin_rotor.imu.gyro[2]))
