
from threading import Thread, Lock

import time
import socket
import numpy as np



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

        if len(received_array) == 1:
            np.save('angle.npy', received_array[0]) # save
            print("Received angle: ", received_array)
        else:
            np.save('steering_torque.npy' , received_array[1])  # save
            print("Received steering torque: ",received_array)
        self.conn.close()
        print("Out of receiver for loop")


def eps_recv():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5004

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

if __name__ == '__main__':
    eps_recv()
