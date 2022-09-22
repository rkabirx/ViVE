# This receives wheel speed, acceleration pedal position and TCS switch status


from threading import Thread,Lock

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

if __name__ == '__main__':
    tcs_recv()