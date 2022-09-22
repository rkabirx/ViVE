
# TCS main program
import threading
from threading import Thread,Lock
import logging
import time
import socket
import numpy as np

lock = Lock()

log = logging.getLogger('can.socketcan.native')
log.debug("Loading native socket can implementation")


class Dual_thread(Thread ):

    def __init__(self,conn ):
        Thread.__init__(self)
        self.conn = conn

    def dissect_can_frame(self,packet ):
        can_id = packet[1]
        print(f"The arbitration id is {can_id}")
        can_bool = packet[0]
        print(f"The extended id is {bool(can_bool)}")
        byte_data = packet[ 2:]
        # print(byte_data)
        data = list(byte_data)
        print(f"The data is {data}")
        return can_id,can_bool,data

    # Current slip rate
    def calculate_SlipRate(self,current_wheel_speed,current_vehicle_speed ):
        slip_rate = ((float(current_wheel_speed) - float(current_vehicle_speed)) * 100) / float(current_vehicle_speed)
        return slip_rate

    def run(self ):

        # Receive Wheel Speed from Sensor

        Acc_position = np.load('acc.npy')
        TCS_stat = np.load('tcs.npy')

        if Acc_position > 0:
            Wheel_Speed = 40
        else:
            Wheel_Speed = np.load('WheelSpeed.npy')
        # Receive Vehicle Speed from ADAS via CANBus

        global myarray
        receiving_completed_flag = 0

        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response

        print('\n')

        print('Starting a new connection')

        packet = self.conn.recv(BUFFER_SIZE1)

        can_id,can_bool,data = self.dissect_can_frame(packet)
        log.debug('Received: can_id=%x, can_bool=%x, Vehicle Speed=%s',can_id,can_bool,data)
        arbitration_id = can_id
        # print(f"arbitration id before passing on is {arbitration_id}")
        lock.acquire()
        myarray = packet  # Add packet elements       # working but override
        print("Closing receiver socket")
        # print(f'final array of vehicle speed is {myarray}')
        self.conn.close()
        # print("Out of receiver for loop")
        receiving_completed_flag = 1
        # print(f'current value of receiving_completed_flag is {receiving_completed_flag}')
        lock.release()

        # Sender socket

        # time.sleep(5)

        if receiving_completed_flag == 1:
            print("Inside sender function")
            TCP_IP = "0.0.0.0"

            TCP_PORT = 5003  # To connect to Hydraulic_modulator.py  # Port of HCU

            BUFFER_SIZE = 1024

            if Acc_position > 0:
                Wheel_Speed = 40
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")
            elif (Acc_position == 0) & (Wheel_Speed == data[0]):
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")
            else:
                Wheel_Speed = data[0]
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")

            if (SlipRate > 0.3) & (Acc_position > 0) & (TCS_stat > 0) :
                # current_pressure = float(pressure) - 1  # Find out whether ECU passes pressure or Change in Pressure to HCU
                torque_reduction = [10]
                print("As Slip rate is higher, torque_reduction is " + str(torque_reduction))
                print("Sending from TCS to CAN Bus")
                # Sending the Pressure data to Central simulator

                from can import Message
                # Here can_msg is the CAN frame to be sent as 3 payloads
                can_msg = Message(is_extended_id=False,arbitration_id=5,data=torque_reduction)
                can_msg2 = Message(is_extended_id=False,arbitration_id=1,data=torque_reduction)

                print(can_msg)  # printing CAN frame
                print(can_msg2)  # printing CAN frame
                # converting is_extended_id to sent via socket
                bool_val = can_msg.is_extended_id
                # Converting boolean to integer
                if bool_val :
                    bool_val = 1
                else :
                    bool_val = 0

                msg_array1 = [bool_val] + [can_msg.arbitration_id] + list(can_msg.data)
                msg_array2 = [bool_val] + [can_msg2.arbitration_id] + list(can_msg2.data)
                Payload1 = bytearray(msg_array1)
                Payload2 = bytearray(msg_array2)
                print("Sending array to ECM: ",msg_array1)
                print("Sending array to gateway: ",msg_array2)
                print("-----------------------------------------------------------------")
                # Sending the CAN frame to CAN simulator via socket

                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                s.send(Payload1)
                data1 = s.recv(BUFFER_SIZE)
                s.close()
                time.sleep(2)

                s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s2.connect((TCP_IP,TCP_PORT))
                s2.send(Payload2)
                data2 = s2.recv(BUFFER_SIZE)
                s2.close()

            else :
                print("Slip rate in range")
                print("-----------------------------------------------------------------")

        return arbitration_id,can_bool,data

class listener_thread(Thread):

    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global myarray

        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response

        print("-----------------------------------------------------------------")
        print('Starting a new connection')

        packet = self.conn.recv(BUFFER_SIZE1)
        received_array = list(packet)
        print("Closing receiver socket")
        print("Received packet: ", received_array)
        # print(len(received_array))
        if len(received_array) == 1:
            np.save('WheelSpeed.npy' , received_array[0])  # save
        elif len(received_array) == 2:
            np.save('tcs.npy', received_array[1]) # save
        else:
            np.save('acc.npy',received_array[2])  # save
        self.conn.close()
        print("Out of receiver for loop")


def tcs_recv():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 6001

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    # log.info('Created a socket')
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:  # Check if this is right -> This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)

        thread2 = listener_thread(conn)
        thread2.start()
def tcs() :
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5062  # It has arbitration ID 6 in dictionary

    ClientCount = 0
    myarray = []

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    log.info('Created a socket')

    # Listener/Receiver section
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True :  # This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)
        thread1 = Dual_thread(conn)
        thread1.start()


if __name__ == '__main__' :
    threading.Thread(target=tcs).start()
    threading.Thread(target=tcs_recv).start()