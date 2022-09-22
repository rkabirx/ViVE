from multiprocessing import Process

import Angle_sensor
import ABS_process
import Torque_sensor

def func1() :
    Angle_sensor.send_angle()

def func2() :
    Torque_sensor.send_torque()

def func3() :
    ABS_process.abs_send()


if __name__ == '__main__' :
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2)
    p2.start()
    p3 = Process(target=func3)
    p3.start()
