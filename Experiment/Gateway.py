

from threading import Thread
from can import Message  # importing CAN frame using python-can library
import socket

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
        datalist = list(packet)

        # can_msg is the assembled CAN frame with received payloads
        can_msg = Message(is_extended_id=bool(datalist[0]),arbitration_id=datalist[1],data=datalist[2])

        print("Assembled CAN frame: ",can_msg)
        if datalist[2] == 100:
            print("Received for Anti-lock braking")
        elif datalist[2] == 10:
            print("Received for traction control")
        elif datalist[2] == 2:
            print("Received for assist and load motor torque")
        elif datalist[2] == 3:
            print("Received for RTC")
        elif datalist[2] == 1:
            print("Received for indirect tire pressure monitoring")
        else:
            print("Error")
        print("-----------------------------------------------------------------")

        self.conn.close()
        print("Out of receiver for loop")


def main():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 7400

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    # log.info('Created a socket')
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:  # Check if this is right -> This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)

        thread = listener_thread(conn)
        thread.start()


if __name__ == '__main__':
    main()




























