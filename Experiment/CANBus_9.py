##### The code which Rafi is using currently

import threading
from threading import Thread,Lock
import socket
import logging
import time
import os
from _thread import *
from queue import Queue
from Simulated_Annealing import *
import random
import math
import copy
from operator import itemgetter

lock = Lock()
queue = Queue()

n = 30  # Column represent the number of threads or number of clients
m = 3  # Row represent the length of the stored data of each client
All_Data = [[] * m] * n
Client_Thread_Count = 0
receiving_completed_flag = 0
Sender_Thread_Count = 1
Sending_Data = [[0] * m] * m

# Receiver Class
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
        # print(f'Value of Client_Thread_count in main function right now at line 166 is {Client_Thread_Count}')
        # lock.acquire()
        # if Client_Thread_Count == random.randint(1,3):
        #     receiving_completed_flag = 1
        #     print("Received all frames -> Array is full -> Ready to start Sender socket")
        # lock.release()


# Sender Class
class Sender_thread(Thread) :

    def __init__(self,s2, TCP_IP, Sending_packets) :
        Thread.__init__(self)
        self.s2 = s2
        self.TCP_IP = TCP_IP
        self.Sending_packets = Sending_packets

    def run(self) :
        global Sender_Thread_Count      # Initialized with 1
        # global Sending_Data
        # TCP_IP = "0.0.0.0"

        dict = {1 : 7400,2 : 5005,3 : 5099,4 : 5062,5 : 5065,6 : 5060,
                7 : 5061}  # To decide the port number of listener as per the received arbitration ID
        print(f'Dictionary is {dict}')

        # Start thread
        lock.acquire()  # Need to acquire lock for Sending_Data values
        arb_id = self.Sending_packets[0][1]
        print(f'arb id to decide port is {arb_id}')
        TCP_PORT = dict[arb_id]

        print(f'Port number from dict is {TCP_PORT}')
        BUFFER_SIZE = 1024

        # s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # try:

        self.s2.connect((self.TCP_IP,TCP_PORT))
        print(f"Connecting sender socket with port {TCP_PORT}")
        # except:
        #     print("Socket already connected")

        print(f'Current Sender thread count is {Sender_Thread_Count}')

        self.s2.send(bytearray(self.Sending_packets[0]))
        # print(Sending_Data[0])
        print(f'Sending data in current thread is {self.Sending_packets[0]}')
        Sender_Thread_Count += 1
        lock.release()
        # self.s2.close()


def main() :
    global receiving_completed_flag
    global All_Data
    global Sending_Data
    global Sender_Thread_Count
    Start_Sending_Flag = 0
    SA_Completed_flag = 0
    Packets = []
    Temp_Array = []
    Sorted_All_Data = []
    Sending_packets = []
    best_sequence = []  # check if I can remove it
    # least_peak_congestion, least_average_congestion = 0
    Sending_Pack_Num = 0

    TCP_IP = "0.0.0.0"
    TCP_PORT = 5003

    ##### Receiver funtion starts from here
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s1.bind((TCP_IP,TCP_PORT))
    except:
        print("Error: Bind failed")

    print('Waiting for a Connection..')
    s1.listen(9)

    Random_num = random.randint(6,9)
    while True :
       # For receiver socket to receive continously
        # try:
        conn,addr = s1.accept()
        conn.setblocking(0)
        s1.setblocking(1)  # prevents timeout
        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        Main_thread_Listen = listener_thread(conn)
        Main_thread_Listen.start()
        Main_thread_Listen.join()
        # except:
        #     print("Unable to accept in receiver socket")

        lock.acquire()
        print(f"Checking Client thread count {Client_Thread_Count} with random num")
        print(f"Random number is {Random_num}")
        if Client_Thread_Count == Random_num:
            receiving_completed_flag = 1
            print("Received all frames successfully for this cycle -> Ready to start Optimizer")
            print("In If loop of receiver to end receiving")
            lock.release()
            break
        else:
            lock.release()
            print("In else loop of receiver to keep on receiving")
            continue

        # s1.close()  ## Check if the socket should be closed in main function or client function
        print('Listener socket closed')

    #---------------------------------------------- Optimizer -------------------------------------------------------------
        #### Reprioritize using optimization function
        time.sleep(1)
        if receiving_completed_flag == 1 :

            print('\n')
            print("Inside Simulated Annealing section")

            # Get_Packet function from here
            Constraint_Dict = {1:3, 2:1, 3:4, 4:2, 5:2, 6:1, 7:2, 8:3, 9:3}
            print(f" Constraint dictionary is {Constraint_Dict}")
            Packet_Dict = {}

            # First try to arrange the whole array with respect to the constraint .i.e. index 1 of each packet
            lock.acquire()      # For Client thread number and All_Data array
            print(f" Client thread count in optimizer code is {Client_Thread_Count}")
            for rows in range(0,Client_Thread_Count):
                print(f"Rows is {rows}")
                Temp_Array.append(All_Data[rows])
            print(f"Temp array is {Temp_Array}")
            lock.release()

            Sorted_All_Data = sorted(Temp_Array, key=itemgetter(1))
            print(f'Sorted Array  of all valid packets is {Sorted_All_Data}')

            # Entering keys in the dictionary as the index of Sorted_All_Data so that each packet has unique key/number
            for i in range(0,len(Sorted_All_Data)):
                Packet_Dict[i]  = Constraint_Dict[Sorted_All_Data[i][1]]  # Value equal to Constraint of the packet as per value in index 1
                Packets.append(i)
                print(f"The constraint of packet number {i} is {Constraint_Dict[Sorted_All_Data[i][1]]} as its arbitration ID is {Sorted_All_Data[i][1]}")
            print(f"Array of Packet numbers is {Packets}") # Create separate array for only packet numbers
            print(f"The packet dictionary is {Packet_Dict}")
            # except:
            #     print("No data in All Data array")

            sa = SimAnneal(Packets, Packet_Dict)
            # Get Best fit sequence in output of this function
            best_sequence, least_peak_congestion, least_average_congestion = sa.Simulated_Anneal()
            # To flag sender socket to start operating
            SA_Completed_flag = 1


            # time.sleep(1)
    #---------------------------------------------- Sender socket-------------------------------------------------------------

        if SA_Completed_flag == 1 :
            print('\n')
            print("Inside Sender function")
            # kk = 0

            #### Packets to be sent in the current cycle
            # Take Sequence[0] (first cycle in the optimized sequence) and get each element in the index
            for pack_num in best_sequence[0]:   # For every packet number in the 1st cycle of best sequence-> Get the packet array
                print(f"1st sub array in best sequence is {best_sequence[0]}")
                print(f"Current loop for pack_num {pack_num}")
                Sending_packets.append(Sorted_All_Data[pack_num])
                # kk += 1
            print(f" Sending packets are {Sending_packets}")    # Now we know which packets are to be passed on to the sender socket

            #### Packets to be passed on to the next cycle
            # Take the sub arrays in best sequence from cycle 2 .i.e. index 1 and override the elements in All_data array

            lock.acquire()  # For all_data array
            All_Data.clear()
            print(f"Cleared All_Data array is {All_Data}")
            for cycles in range(1, len(best_sequence)-1):
                # if cycles> 1:   # because 1st cycle will be passed on to the sender
                print(f"Current cycle in for loop is {cycles}")
                for pack_num in best_sequence[cycles]: # to access each element/packet number in sub arrays
                    print(f"other sub array in best sequence is {best_sequence[cycles]}")
                    print(f"Current loop for pack_num {pack_num}")
                    All_Data[Sending_Pack_Num].append(Sorted_All_Data[pack_num])
                    print(f"Packet added to All Data array is {Sorted_All_Data[pack_num]}")
                    Sending_Pack_Num += 1
            print(f"All_Data array for next cycle is {All_Data}")
            lock.release()

            # Create sender socket connection
            TCP_IP = "0.0.0.0"
            s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


            print("In while loop")
            Main_thread_Send = Sender_thread(s2, TCP_IP, Sending_packets)
            Main_thread_Send.daemon = True
            Main_thread_Send.start()
            Main_thread_Send.join()
            lock.acquire()
            if Sender_Thread_Count == Sending_Pack_Num:
                print(f"Number of sender threads are {Sender_Thread_Count} is equal to Number of packets to be sent .i.e. {Sending_Pack_Num}, hence stop sending packets")
                lock.release()
                break
            else:
                print("In else loop of sender to continue sending packets")
                lock.release()
                continue


            print("All Data Sent")
            ## Check if the socket should be closed in main function or client function
            s2.close()
            print('Sender socket closed')


if __name__ == '__main__' :
    main()








########### My old working code

# import threading
# from threading import Thread, Lock
# import socket
# import logging
# import time
# import os
# from _thread import *
# from queue import Queue
#
# lock = Lock()
# queue = Queue()
#
# n = 12 # Rows represent the number of threads or number of clients
# m = 15 # Column represent the length of the stored data of each client
# All_Data = [[0] * m] * n
# Reprioritized_frames = [[0] * m] * n
# Client_Thread_Count = 0
# receiving_completed_flag = 0
# Sender_Thread_Count = 1
# Sending_Data = [[0] * m] * m
#
#
# class listener_thread(Thread):
#
#     def __init__(self, conn):
#         Thread.__init__(self)
#         self.conn = conn
#         # self.Client_Thread_Count = Client_Thread_Count
#
#     def dissect_can_frame(self, packet):
#         can_id = packet[1]
#         print(f"The arbitration id is {can_id}")
#         can_bool = packet[0]
#         print(f"The extended id is {bool(can_bool)}")
#         byte_data = packet[2:]
#         # print(byte_data)
#         data = list(byte_data)
#         print(f"The data is {data}")
#         return can_id,can_bool,data
#
#     def run(self):
#
#         # receiving_completed_flag = 0
#         temp_array = []
#         global All_Data
#         global Client_Thread_Count
#         global receiving_completed_flag
#
#         BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response
#
#         print('\n')
#         print("-----------------------------------------------------------------")
#         print('Starting a new connection')
#
#         packet = self.conn.recv(BUFFER_SIZE1)
#
#         can_id, can_bool, data = self.dissect_can_frame(packet)
#         # log.debug('Received: can_id=%x, can_bool=%x, data=%s', can_id, can_bool, data)
#         # arbitration_id = can_id
#         # if arbitration_id > 6:
#         #     time.sleep(3)
#         # else:
#         #     pass
#         # print(f"arbitration id before passing on is {arbitration_id}")
#
#         lock.acquire()      # Acquire lock for All_Data array and self.Client_Thread_Count
#         # Current_Client_Thread_Number = Client_Thread_Count
#         # print(f'Current client thread number is {Client_Thread_Count}')
#
#         temp_array = list(packet)
#         # print(f'The packet in current frame is {temp_array}')
#         All_Data[Client_Thread_Count] = temp_array
#         print(f'Updated All_Data array is {All_Data}')
#         Client_Thread_Count += 1
#         print(f'Client thread number is {Client_Thread_Count}')
#
#         from can import Message
#         can_msg = Message(is_extended_id=bool(packet[0]),arbitration_id=packet[1],data=packet[2:])
#         # print("Assembled CAN frame: ",can_msg)
#
#         print("Closing receiver connection")
#         self.conn.close()
#         lock.release()
#
#
# class Sender_thread(Thread):
#
#     def __init__(self, conn):
#         Thread.__init__(self)
#         self.conn = conn
#
#     def run(self):
#             global Sender_Thread_Count
#             global Sending_Data
#             TCP_IP = "0.0.0.0"
#
#             dict = {1: 5004, 2: 5005, 3: 5099, 4: 5062, 5: 5065, 6: 5060, 7: 5061}    # To decide the port number of listener as per the received arbitration ID
#             print(f'Dictionary is {dict}')
#
#             # Start thread
#             lock.acquire()      # Need to acquire lock for Sending_Data values
#             arb_id = Sending_Data[0][1]
#             print(f'arb id to decide port is {arb_id}')
#             TCP_PORT = dict[arb_id]
#
#             print(f'Port number from dict is {TCP_PORT}')
#             BUFFER_SIZE = 1024
#
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.connect((TCP_IP, TCP_PORT))
#             print(f"Connecting sender socket with port {TCP_PORT}")
#
#             print(f'Current Sender thread count is {Sender_Thread_Count}')
#             print("--------------------------------------------------------")
#             s.send(bytearray(Sending_Data[0]))
#             Sender_Thread_Count +=1
#             lock.release()
#             s.close()
#
# def Reprioritize_SA():
#
#
# def main():
#
#     global receiving_completed_flag
#     global All_Data
#     global Sending_Data
#     Start_Sending_Flag = 0
#
#     # while(1):
#     TCP_IP = "0.0.0.0"
#     TCP_PORT = 5003
#
#     ##### Receiver funtion starts from here
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     try:
#         s.bind((TCP_IP, TCP_PORT))
#     except socket.error as e:
#         print(str(e))
#
#     print('Waiting for a Connection..')
#     s.listen(5)
#
#     while receiving_completed_flag != 1:
#         conn, addr = s.accept()
#         s.setblocking(1)  # prevents timeout
#         print('Connected to: ' + addr[0] + ':' + str(addr[1]))
#
#         Main_thread_Listen = listener_thread(conn, )
#         Main_thread_Listen.start()
#         Main_thread_Listen.join()
#
#         lock.acquire()
#         # print(f'Value of Client_Thread_count in main function right now at line 166 is {Client_Thread_Count}')
#         if Client_Thread_Count == 11:
#             receiving_completed_flag = 1
#             print("Received all frames -> Array is full -> Ready to start Sender socket")
#         lock.release()
#
#     s.close()               ## Check if the socket should be closed in main function or client function
#     print('Listener socket closed')
#
#     # #### Take Decision
#     # lock.acquire()
#     # if receiving_completed_flag == 1 & All_Data:   # If All data is received and All_Data is not empty
#     #     if Client_Thread_Count == 1:               # Condition to "Send"
#     #         Start_Sending_Flag = 1
#     #     elif Client_Thread_Count > 1:
#     #         Reprioritize_SA()
#     # else:
#     #     Start_Sending_Flag = 0
#     #
#     # lock.release()
#     #
#     # #### Reprioritize using optimization function
#     #
#
#
#
#     ######## Sender socket
#     if receiving_completed_flag == 1:
#         print('\n')
#         print("Inside Sender function")
#
#         ## Start threads
#         for i in range(Client_Thread_Count):
#             k =0
#             # print(f'The current value of i in 1st for loop is {i}')
#             for j in range(len(All_Data[i])):
#                 # print(f'The current value of j in 2nd for loop is {j}')
#                 lock.acquire()
#                 # print(f'The value to be transfered now is {All_Data[i][j]}')
#                 Sending_Data[0][k] = All_Data[i][j]
#                 # print(f'The value saved in Sending_Data at {k} index is {Sending_Data[0][k]}')
#                 k += 1
#                 # print(f'The incremented value of k is {k}')
#                 # print(f'Sending data in current sending thread in main function is {Sending_Data}')
#                 lock.release()
#             print(f'Sending data in current thread is {Sending_Data[0]}')
#             Main_thread_Send = Sender_thread(conn, )
#             Main_thread_Send.daemon = True
#             Main_thread_Send.start()
#             Main_thread_Send.join()
#
#     print("All Data Sent")
#     s.close()               ## Check if the socket should be closed in main function or client function
#     print('Sender socket closed')
#
#
#
# if __name__ == '__main__':
#     main()
#



