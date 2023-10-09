import os
import can


class Motor:

    CONVERSION_FACTOR = 0.01 #dps/LSB
    #constructor
    def __init__(self):

        #M0 CAN ID
        self.motor0ID = 0x141

        #M1 CAN ID
        self.motor1ID = 0x142

        #Speed control command ID
        self.speedControlCommandID = 0xA2

    	#Motor off command ID
        self.motorOffID = 0x80

        #Motor stop command ID
        self.motorStopID = 0x81

        #Motor run command ID
        self.motoRunID = 0x88

        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')

        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')#type: ignore

        pass

    def __del__(self):
        self._speedControlM1(0)
        self._speedControlM0(0)
        self.can0.shutdown()
        os.system('sudo ifconfig can0 down')

    @classmethod
    def _convert_speed(cls,speed):
        speed_dps = speed*360/60
        raw_speed = speed_dps/0.01
        return int(raw_speed)

    
    def set_speed_M0(self,speed_rpm):
        self._speedControlM0(self._convert_speed(speed_rpm))

    def set_speed_M1(self,speed_rpm):
        self._speedControlM1(self._convert_speed(speed_rpm))

    def _speedControlM0(self, speed):

        byte1 = speed & 0xFF
        byte2 = (speed & 0xFF00) >> 8
        byte3 = (speed & 0xFF0000) >> 16
        byte4 = (speed & 0xFF000000) >> 24
        
        # print(byte1)
        # print(byte2)
        # print(byte3)
        # print(byte4)

        msg = can.Message(arbitration_id = self.motor0ID, data = [self.speedControlCommandID, 0, 0, 0, byte1, byte2, byte3, byte4], is_extended_id=False)
        self.can0.send(msg)

    def _speedControlM1(self, speed):

        byte1 = speed & 0xFF
        byte2 = (speed & 0xFF00) >> 8
        byte3 = (speed & 0xFF0000) >> 16
        byte4 = (speed & 0xFF000000) >> 24
        
        # print(byte1)
        # print(byte2)
        # print(byte3)
        # print(byte4)

        msg = can.Message(arbitration_id = self.motor1ID, data = [self.speedControlCommandID, 0, 0, 0, byte1, byte2, byte3, byte4], is_extended_id=False)
        self.can0.send(msg)

    def turnOffM0(self):

        msg = can.Message(arbitration_id = self.motor0ID, data = [self.motorOffID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)

    def turnOffM1(self):

        msg = can.Message(arbitration_id = self.motor1ID, data = [self.motorOffID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)

    def stopM0(self):

        msg = can.Message(arbitration_id = self.motor0ID, data = [self.motorStopID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)

    def stopM1(self):

        msg = can.Message(arbitration_id = self.motor1ID, data = [self.motorStopID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)

    def runM0(self):

        msg = can.Message(arbitration_id = self.motor0ID, data = [self.motoRunID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)

    def runM1(self):

        msg = can.Message(arbitration_id = self.motor1ID, data = [self.motoRunID, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
        self.can0.send(msg)
