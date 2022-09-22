
from threading import Thread

import socket
import time

class Dual_thread(Thread):

    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn

    def iTCPMS_send(self, x):
        TCP_IP = "0.0.0.0"
        TCP_PORT = 5003
        BUFFER_SIZE = 1024

        pressure_status = [x]

        from can import Message
        can_msg = Message(is_extended_id=False,arbitration_id=1,data=pressure_status)
        print(can_msg)  # printing CAN frame

        # converting is_extended_id to sent via socket
        bool_val = can_msg.is_extended_id
        # Converting boolean to integer
        if bool_val:
            bool_val = 1
        else:
            bool_val = 0

        Payload1 = [bool_val]
        Payload2 = [can_msg.arbitration_id]
        Payload3 = list(can_msg.data)

        msg_array = Payload1 + Payload2 + Payload3

        Payload = bytearray(msg_array)
        print("Sending payload: ",msg_array)

        # Sending the CAN frame to CAN simulator via socket

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((TCP_IP,TCP_PORT))
        s.send(Payload)
        data1 = s.recv(BUFFER_SIZE)
        s.close()
        time.sleep(2)

    def run(self):
        receiving_completed_flag = 1

        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response
        print('-------------------------------------------------------')
        print('Starting a new connection')
        packet = self.conn.recv(BUFFER_SIZE1)
        self.conn.close()
        receiving_completed_flag = 1

        tire_diameters = list(packet)

        tire1_circumference = tire_diameters[0] * 3.1416
        tire2_circumference = tire_diameters[1] * 3.1416
        tire3_circumference = tire_diameters[2] * 3.1416
        tire4_circumference = tire_diameters[3] * 3.1416

        tire_threshold = 47 * 0.75  # 25% of 47 circumference

        print("The tire circumferences are: %s, %s, %s and %s" % (tire1_circumference,tire2_circumference,tire3_circumference,tire4_circumference))

        print("Tire circumference threshold: ",tire_threshold)
        if receiving_completed_flag == 1:
            if (tire1_circumference or tire2_circumference or tire3_circumference or tire4_circumference) < tire_threshold:
                print('Tire pressure in range')
                #self.iTCPMS_send(0)
            else:
                print("Low tire pressure!")
                self.iTCPMS_send(1)
        return tire_diameters


def tpms():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5093

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    # log.info('Created a socket')
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:  # Check if this is right -> This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)

        thread = Dual_thread(conn)
        thread.start()

if __name__ == '__main__':
    tpms()
