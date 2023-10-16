from Orise_Twin_Rotor import PID
from Orise_Twin_Rotor import Twin_Rotor
from time import sleep
from Orise_Twin_Rotor import Data_Buffers
from Orise_Twin_Rotor import Create_Gui, READING_NAMES
from Orise_Twin_Rotor import CSV_Logger
import numpy as np
import math
from time import time

MAX_SPEED = 600*6
Kp = 0.342
Kd = 0.222
Ki = 0.132


## NEw VALUES FOR DYNAMIC SYSTEM######
Ki = 0.6
Kd = 0.5
######################################

Limits = (-MAX_SPEED//2, MAX_SPEED//2)
constant = MAX_SPEED//2


class Stable_Contoller:
    '''
    Helper class to constrol the system and do PID
    '''

    def __init__(self):
        self.twin_rotor = Twin_Rotor()
        self.pid = PID(Kp, Ki, Kd, Limits, derivative_filter_omega=5,
                       derivative_on_measurement=True)
        self.angle = 0
        self.beta = 1.0

    def __del__(self):
        self.twin_rotor.stop()

    def set_set_point(self, point):
        self.pid.set_set_point(point)

    def run(self):
        # update readings and get the time elapsed
        time_delta = self.twin_rotor.update_readings()
        angle = self.twin_rotor.imu.simple_pitch_from_g_fusion  # get the pitch
        if(abs(angle) < math.radians(50)):  # filter outliers
            self.angle = angle*(self.beta)+self.angle * \
                (1-self.beta)  # do some low pass filtering
        # scale control signal
        val = MAX_SPEED/2*self.pid(self.angle, time_delta)

        self.twin_rotor.motors.set_speed(
            constant+val, -constant+val)  # set the speed
        return val


def dynamic_set_point_sin(t):
    ''' Create a sin wave control signal'''
    f = 0.1
    return math.radians(15)*math.sin(2*math.pi*f*t)


def dynamic_set_point_square(t):
    ''' Create a square pulse control signal'''
    f = 0.05
    return (t % (1/f) > (1/f/2))*math.radians(30)


def main():
    FILE_PATH = "logging_test/csv_data_logger.csv"  # path to the log file
    # creating a logger to log sensor data as a csv file
    data_logger = CSV_Logger(FILE_PATH)
    controller = Stable_Contoller()
    controller.set_set_point(0)
    # creating data buffers to sotre sensor data to be used by the plot -- 1000 data point history will be recorded
    data_buffers = Data_Buffers(1000)
    # create a custom buffer to store you own calculated data
    custom_buffers = data_buffers.get_custom_buffer()
    # create a custom buffer to store you own calculated data
    fitlered_vale = data_buffers.get_custom_buffer()
    gui_application = Create_Gui(data_buffers)  # create the gui
    # add encoder value to a plit called encoder1
    gui_application.add_time_graph("encoder1", lambda x: x.encoder1.data)
    gui_application.add_twin_rotor_data(
        "mag", READING_NAMES.MAG_X, (255, 0, 0), "mag_x")  # add mag_z to a plot called mag
    gui_application.add_twin_rotor_data(
        "mag", READING_NAMES.MAG_Y, (0, 255, 0), "mag_y")  # repeat for mag_y and mag_z
    # mag_x,mag_y and mag_z will all be plotted in the same plot ("mag")
    gui_application.add_twin_rotor_data(
        "mag", READING_NAMES.MAG_Z, (0, 0, 255), "mag_z")
    gui_application.add_custom_buffer_graph(
        "pitch", fitlered_vale, (255, 0, 0), "filtered_value")  # plot the filtered pitch value
    # plot the set point both the set point and filterd value will be drawn on the same plot ("pitch")
    gui_application.add_custom_buffer_graph(
        "pitch", custom_buffers, (0, 255, 0), "set_point")
    gui_application.start()
    t = time()
    while True:
        # update the data buffers to plot the sensor data
        data_buffers.update_buffers(controller.twin_rotor)
        controller.run()
        data_logger.log(controller.twin_rotor)  # log raw sensor data
        point = dynamic_set_point_sin(time()-t)
        # push valus to the custom buffer -- (if you don't do this the plots won't update)
        custom_buffers.push(point)
        # push valus to the custom buffer -- (if you don't do this the plots won't update)
        fitlered_vale.push(controller.angle)
        controller.set_set_point(point)
        if not gui_application.active:
            break
        sleep(0.001)


if __name__ == "__main__":
    main()
