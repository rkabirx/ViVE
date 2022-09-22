from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os
import serial
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib import pyplot as pllt

import time

picar.setup()
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable = True
draw_circle_enable = True
scan_enable = False
rear_wheels_enable = True
front_wheels_enable = True
pan_tilt_enable = True

if (show_image_enable or draw_circle_enable) and "DISPLAY" not in os.environ:
    print('Warning: Display not found, turn off "show_image_enable" and "draw_circle_enable"')
    show_image_enable = False
    draw_circle_enable = False

kernel = np.ones((5, 5), np.uint8)
img = cv2.VideoCapture(-1)

SCREEN_WIDTH = 160
SCREEN_HIGHT = 120
img.set(3, SCREEN_WIDTH)
img.set(4, SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HIGHT / 2
BALL_SIZE_MIN = SCREEN_HIGHT / 10
BALL_SIZE_MAX = SCREEN_HIGHT / 3

# Filter setting, DONOT CHANGE
hmn = 12
hmx = 37
smn = 96
smx = 255
vmn = 186
vmx = 255

follow_mode = 1

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX = 170
PAN_ANGLE_MIN = 10
TILT_ANGLE_MAX = 150
TILT_ANGLE_MIN = 70
FW_ANGLE_MAX = 90 + 30
FW_ANGLE_MIN = 90 - 30

SCAN_POS = [[20, TILT_ANGLE_MIN], [50, TILT_ANGLE_MIN], [90, TILT_ANGLE_MIN], [130, TILT_ANGLE_MIN],
            [160, TILT_ANGLE_MIN],
            [160, 80], [130, 80], [90, 80], [50, 80], [20, 80]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)

motor_speed = 60

# Baud_Rate = 9600

# ser = serial.Serial('/dev/ttyACM0',Baud_Rate)      # Added for attack

# Distance_List = []


def nothing(x):
    pass


def Get_Sensor_Data(Baud_Rate):
    pan_angle = 90  # initial angle for pan
    tilt_angle = 90  # initial angle for tilt
    fw_angle = 90

    Min_Distance = 5

    scan_count = 0

    ser = serial.Serial('/dev/ttyACM0', Baud_Rate)  # Added for attack    # Shifted from line 84

    print("Begin!")

    while True:

        print("Starting to read from Arduino")
        read_serial = ser.readline()

        Current_Distance = int(ser.readline(), 16)
        print(Current_Distance)

        # if Current_Distance > Min_Distance:
        if Current_Distance == 0:
            # follow_mode == 1
            bw.speed = motor_speed
            # bw.forward()
            bw.backward()
            print(f"moving ahead as the current distance is {Current_Distance}")
        else:
            bw.stop()
            print(f"Car stopped as distance received is {Current_Distance}")

        # Rafi's version ------------
        Time_List = [0, 5, 10, 15, 20, 25]
        Distance_List = list(range(1, 31, 5))
        fig1 = plt.figure(1, figsize=(8, 7))

        if len(Distance_List) == 6:
            plt.plot(Time_List, Distance_List, 'g', label="Distance values without Attack")
            plt.axis([0, 30, 0, 40])
            plt.ylabel("Distance", size="15")
            plt.xlabel("Time", size="15")
            plt.legend(fontsize="15", edgecolor="black")
            plt.show()


        ## Plot distance values to compare in the end with attacked distance array
        #         Distance_List.append(Current_Distance)
        #
        #         fig1 = plt.figure(1, figsize = (10,10))
        #
        #         if len(Distance_List) == 30:
        #             plt.plot(Time_List, Distance_List, 'g', label = "Distance values without Attack")
        #             plt.ylabel("Distance", size = "30")
        #             plt.xlabel("Time", size = "30")
        #             plt.xlim(0, 31, 1)
        #             plt.ylim(0, 31, 1)
        #             plt.legend(fontsize = "20", edgecolor = "black")
        #             plt.show()
        #             #time.sleep(1)
        #             Distance_List.clear()

        Current_Distance = 0
        print("Restarting while loop now")


def destroy():
    bw.stop()
    print(f"Car stopped as distance received is {Current_Distance}")


def test():
    fw.turn(90)

# if __name__ == '__main__':
#
#     #ser = serial.Serial('/dev/ttyACM0',Baud_Rate)      # Added for attack
#
#     try:
#         Get_Sensor_Data(Baud_Rate)
#     except KeyboardInterrupt:
#         destroy()