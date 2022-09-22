from multiprocessing import Process

import WheelSpeed_sensor
import ADAS
import TCS_switch
import Acc_pedal

def func1() :
    TCS_switch.tcs()

def func2() :
    Acc_pedal.acc_pedal(6001)

def func3() :
    WheelSpeed_sensor.send(6001) # In this way, can change port numbers for different use cases


def func4() :
    ADAS.adas(4) # In this way, can change arb id for different use cases



if __name__ == '__main__' :
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2)
    p2.start()
    p3 = Process(target=func3)
    p3.start()
    p4 = Process(target=func4)
    p4.start()
