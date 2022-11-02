# Working on Vehicle speed line 36 -> goal is to get vehicle speed in data section as per CANBus similarity -> This will just replace numpy line of ABS_process_copy.py -> Next step is to do calculation of slip rate in the same thread and then send pressure in sender socket
# Not able to decide which port number to write in line 119 as this code is stuck at receiving connection from its sender


# ABS main program
import threading
from threading import Thread,Lock
import socket
import logging
import time
import socket
import numpy as np

lock = Lock()

log = logging.getLogger('can.socketcan.native')
log.debug("Loading native socket can implementation")


class Dual_thread(Thread):

    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn

    def dissect_can_frame(self,packet):
        can_id = packet[1]
        print(f"The arbitration id is {can_id}")
        can_bool = packet[0]
        print(f"The extended id is {bool(can_bool)}")
        byte_data = packet[2:]
        # print(byte_data)
        data = list(byte_data)
        print(f"The data is {data}")
        return can_id,can_bool,data


    def run(self):


        global myarray
        receiving_completed_flag = 0

        BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

        print('\n')

        print('Starting a new connection')

        packet = self.conn.recv(BUFFER_SIZE)
        can_id, can_bool, data = self.dissect_can_frame(packet)
        lock.acquire()  # Acquire lock for All_Data array and self.Client_Thread_Count

        from can import Message
        can_msg = Message(is_extended_id=bool(packet[0]), arbitration_id=packet[1], data=packet[2:])
        print("Assembled CAN frame: ",can_msg)
        print("Closing receiver connection")
        self.conn.close()
        receiving_completed_flag = 1
        lock.release()

        # Sender socket
        import time
        time.sleep(1)
        print("-----------------------------------------------------------------")
        if receiving_completed_flag == 1:
            print("Inside sender function")
            TCP_IP = "0.0.0.0"

            dict = {1: 7400, 2: 5005, 3: 5099, 4: 5062, 5: 5065, 6: 5060,
                    7: 5061}  # To decide the port number of listener as per the received arbitration ID
            print(f'Dictionary is {dict}')

            # lock.acquire()  # Need to acquire lock for Sending_Data values
            arb_id = packet[1]
            print(f'arb id to decide port is {arb_id}')
            TCP_PORT = dict[arb_id]
            print(f'Port number from dict is {TCP_PORT}')


            # Here can_msg is the CAN frame to be sent as 3 payloads
            # can_msg = Message(is_extended_id=False,arbitration_id=1,data=[Pressure])
            print(can_msg)  # printing CAN frame
            # converting is_extended_id to sent via socket
            bool_val = can_msg.is_extended_id
            # Converting boolean to integer
            if bool_val:
                bool_val = 1
            else:
                bool_val = 0

            Payload1 = [bool_val]
            Payload2 = [arb_id]
            Payload3 = list(can_msg.data)
            msg_array = Payload1 + Payload2 + Payload3
            Payload = bytearray(msg_array)

            print("Sending array: ",msg_array)

            # Sending the CAN frame to CAN simulator via socket

            s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s2.connect((TCP_IP,TCP_PORT))
            print(f"Connecting sender socket with port {TCP_PORT}")
            s2.send(Payload)
            data1 = s2.recv(BUFFER_SIZE)
            s2.close()
            print("-----------------------------------------------------------------")
        else:
            print("Slip rate in range" )
            print("-----------------------------------------------------------------")

        return can_id,can_bool,data



def main():
    print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"Starting new cycle: Cycle number")
    print("Inside receiver socket")
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5003

    ClientCount = 0
    myarray = []

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    log.info('Created a socket')

    # Listener/Receiver section
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:  # This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)
        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        thread1 = Dual_thread(conn)
        thread1.start()


if __name__ == '__main__':
    main()