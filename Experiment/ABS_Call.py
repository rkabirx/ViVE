import threading

import subprocess
from multiprocessing import Process

import time

stream_lock = threading.Lock()

def server_func():
    # subprocess.run("python3 CANBus_5.py & python3 ABS_process.py & python3 Hydraulic_modulator.py & python3 Gateway.py", shell=True)
    subprocess.run("python3 CANBus_april21.py & python3 ABS_process.py & python3 Hydraulic_modulator.py & python3 Gateway.py", shell=True)

def client_func():
    import WheelSpeed_sensor
    import ADAS
    import Brake_pedal

    def func1():
        WheelSpeed_sensor.send(5005)  # In this way, can change port numbers for different use cases

    def func2():
        ADAS.adas(6)  # In this way, can change arb id for different use cases

    def func3():
        Brake_pedal.brake_send(5005)

    if __name__ == '__main__':
        p1 = Process(target=func1)
        p1.start()
        p2 = Process(target=func2)
        p2.start()
        p3 = Process(target=func3)
        p3.start()

t_server = threading.Thread(target=server_func).start()

# time.sleep(3)
t_client = threading.Thread(target=client_func).start()
