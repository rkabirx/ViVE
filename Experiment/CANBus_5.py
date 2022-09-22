import threading
from threading import Thread,Lock
import socket
import logging
import time
import os
from _thread import *
from queue import Queue

lock = Lock()
queue = Queue()

n = 100  # Rows represent the number of threads or number of clients
m = 3  # Column represent the length of the stored data of each client
All_Data = [[0] * m] * n
Client_Thread_Count = 0
receiving_completed_flag = 0
Sender_Thread_Count = 1
Sending_Data = [[0] * m] * m


class listener_thread(Thread) :

    def __init__(self,conn) :
        Thread.__init__(self)
        self.conn = conn
        # self.Client_Thread_Count = Client_Thread_Count

    def dissect_can_frame(self,packet) :
        can_id = packet[1]
        print(f"The arbitration id is {can_id}")
        can_bool = packet[0]
        print(f"The extended id is {bool(can_bool)}")
        byte_data = packet[2 :]
        # print(byte_data)
        data = list(byte_data)
        print(f"The data is {data}")
        return can_id,can_bool,data

    def run(self) :
        # receiving_completed_flag = 0
        temp_array = []
        global All_Data
        global Client_Thread_Count
        global receiving_completed_flag

        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response

        print('\n')
        print("-----------------------------------------------------------------")
        print('Starting a new connection')

        packet = self.conn.recv(BUFFER_SIZE1)

        can_id,can_bool,data = self.dissect_can_frame(packet)
        # log.debug('Received: can_id=%x, can_bool=%x, data=%s', can_id, can_bool, data)
        # arbitration_id = can_id
        # if arbitration_id > 6:
        #     time.sleep(3)
        # else:
        #     pass
        # print(f"arbitration id before passing on is {arbitration_id}")

        lock.acquire()  # Acquire lock for All_Data array and self.Client_Thread_Count
        # Current_Client_Thread_Number = Client_Thread_Count
        # print(f'Current client thread number is {Client_Thread_Count}')

        temp_array = list(packet)
        # print(f'The packet in current frame is {temp_array}')
        All_Data[Client_Thread_Count] = temp_array
        print(f'Updated All_Data array is {All_Data}')
        Client_Thread_Count += 1
        print(f'Client thread number is {Client_Thread_Count}')

        from can import Message
        can_msg = Message(is_extended_id=bool(packet[0]),arbitration_id=packet[1],data=packet[2 :])
        # print("Assembled CAN frame: ",can_msg)

        print("Closing receiver connection")
        self.conn.close()
        lock.release()



class Sender_thread(Thread) :

    def __init__(self,conn) :
        Thread.__init__(self)
        self.conn = conn

    def run(self) :
        global Sender_Thread_Count
        global Sending_Data
        TCP_IP = "0.0.0.0"

        dict = {1 : 7400,2 : 5005,3 : 5099,4 : 5062,5 : 5065,6 : 5060,
                7 : 5061, 9: 5099}  # To decide the port number of listener as per the received arbitration ID
        print(f'Dictionary is {dict}')

        # Start thread
        lock.acquire()  # Need to acquire lock for Sending_Data values
        arb_id = Sending_Data[0][1]
        print(f'arb id to decide port is {arb_id}')
        TCP_PORT = dict[arb_id]

        print(f'Port number from dict is {TCP_PORT}')
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((TCP_IP,TCP_PORT))
        print(f"Connecting sender socket with port {TCP_PORT}")

        print(f'Current Sender thread count is {Sender_Thread_Count}')

        s.send(bytearray(Sending_Data[0]))
        # print(Sending_Data[0])
        print(f'Sending data in current thread is {Sending_Data[0]}')
        Sender_Thread_Count += 1
        lock.release()
        s.close()


def main() :
    global receiving_completed_flag
    global All_Data
    global Sending_Data
    Start_Sending_Flag = 0

    TCP_IP = "0.0.0.0"
    TCP_PORT = 5003

    ##### Receiver funtion starts from here
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))

    print('Waiting for a Connection..')
    s.listen(2)

    while True :
        conn,addr = s.accept()
        conn.setblocking(0)
        s.setblocking(1)  # prevents timeout
        print('Connected to: ' + addr[0] + ':' + str(addr[1]))

        Main_thread_Listen = listener_thread(conn)
        Main_thread_Listen.start()
        Main_thread_Listen.join()

        lock.acquire()
        # print(f'Value of Client_Thread_count in main function right now at line 166 is {Client_Thread_Count}')
        if Client_Thread_Count == 2 :
            receiving_completed_flag = 1
            print("Received all frames -> Array is full -> Ready to start Sender socket")
        lock.release()

        # s.close()  ## Check if the socket should be closed in main function or client function
        print('Listener socket closed')

        #### Take Decision
        # lock.acquire()
        # if receiving_completed_flag == 1 & All_Data:   # If All data is received and All_Data is not empty
        #     if Client_Thread_Count == 1:               # Condition to "Send"
        #         Start_Sending_Flag = 1
        #     elif
        #
        # else:
        #     Start_Sending_Flag = 0

        #### Reprioritize using optimization function
        # time.sleep(1)
        ######## Sender socket
        if receiving_completed_flag == 1 :
            print('\n')
            print("Inside Sender function")

            # Start threads
            for i in range(Client_Thread_Count) :
                k = 0
                # print(f'The current value of i in 1st for loop is {i}')
                for j in range(len(All_Data[i])) :
                    # print(f'The current value of j in 2nd for loop is {j}')
                    lock.acquire()
                    # print(f'The value to be transfered now is {All_Data[i][j]}')
                    Sending_Data[0][k] = All_Data[i][j]
                    # print(f'The value saved in Sending_Data at {k} index is {Sending_Data[0][k]}')
                    k += 1
                    # print(f'The incremented value of k is {k}')
                    # print(f'Sending data in current sending thread in main function is {Sending_Data}')
                    lock.release()

            Main_thread_Send = Sender_thread(conn)
            Main_thread_Send.daemon = True
            Main_thread_Send.start()
            Main_thread_Send.join()

        print("All Data Sent")
        ## Check if the socket should be closed in main function or client function
        print('Sender socket closed')


if __name__ == '__main__' :
    main()

