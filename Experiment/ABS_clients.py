from multiprocessing import Process

import WheelSpeed_sensor
import ADAS
import Brake_pedal

def func1() :
    WheelSpeed_sensor.send(5005) # In this way, can change port numbers for different use cases

def func2() :
    ADAS.adas(6)  # In this way, can change arb id for different use cases

def func3() :
    Brake_pedal.brake_send(5005)


if __name__ == '__main__' :
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2)
    p2.start()
    p3 = Process(target=func3)
    p3.start()
