import board
import adafruit_icm20x
import math


class IMU:
    def __init__(self):
        self._i2c   = board.I2C()
        self._icm = adafruit_icm20x.ICM20948(self._i2c)
        self._acceleration = self._icm.acceleration
        self._gyro = self._icm.gyro


    @property
    def acceleration(self):
        return self._acceleration
    
    @property
    def gyro(self):
        return self._gyro

    def update(self):
        self._acceleration = self._icm.acceleration
        self._gyro = self._icm.gyro

    @property
    def simple_pitch_from_g_fusion(self):
        '''
        simply finding the pitch using atan2(x,z)
        '''
        x,y,z = self.acceleration
        return math.atan2(x,z)

    def acceleration_string(self):
        return f"acc.x={self.acceleration[0]} acc.y={self.acceleration[1]} acc.z={self.acceleration[2]}"

    def gyro_string(self):
        return f"gyro.x={self.acceleration[0]} gyro.y={self.acceleration[1]} gyro.z={self.acceleration[2]}"

    def __str__(self):
        return f"{self.acceleration_string()} {self.gyro_string()}"

    def __repr__(self):
        return self.__str__()

        
def two_decimal_places(values):
    return " ".join(f"{val:.2f}" for val in values)
def main():
    imu = IMU()
    while True:
        print(imu.simple_pitch_from_g_fusion)
        print(two_decimal_places(imu.acceleration),two_decimal_places(imu.gyro))


if __name__ == "__main__":
    main()