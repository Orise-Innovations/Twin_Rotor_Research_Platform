import board
import adafruit_icm20x
import math


class IMU:
    def __init__(self):
        self._i2c   = board.I2C()
        self._icm = adafruit_icm20x.ICM20948(self._i2c)

    @property
    def acceleration(self):
        return self._icm.acceleration
    
    @property
    def gyro(self):
        return self._icm.gyro

    @property
    def simple_pitch_from_g_fusion(self):
        '''
        simply finding the pitch using atan2(x,z)
        '''
        x,y,z = self.acceleration
        return math.atan2(x,z)
        
        

        
def two_decimal_places(values):
    return " ".join(f"{val:.2f}" for val in values)
def main():
    imu = IMU()
    while True:
        print(imu.simple_pitch_from_g_fusion)
        # print(two_decimal_places(imu.acceleration),two_decimal_places(imu.gyro))


if __name__ == "__main__":
    main()