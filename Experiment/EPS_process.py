
# EPS process for Right turn, high speed


from threading import Thread, Lock
import threading
import logging
import time
import socket
import numpy as np

lock = Lock()

log = logging.getLogger('can.socketcan.native')
log.debug("Loading native socket can implementation")

class Dual_thread(Thread):

    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def dissect_can_frame(self, packet):
        can_id = packet[1]
        print(f"The arbitration id is {can_id}")
        can_bool = packet[0]
        print(f"The extended id is {bool(can_bool)}")
        byte_data = packet[2:]
        # print(byte_data)
        data = list(byte_data)
        print(f"The data is {data}")
        return can_id, can_bool, data

#  socket connection for sending assist torque and load torque to motors
    def torque_send(self, x, y):
        TCP_IP = "0.0.0.0"  # IP of laptop
        BUFFER_SIZE = 1024
        print("Sending from EPS to Assist motor and Load motor")

        TCP_PORT25 = 5025
        assist_send = bytearray([x])  # converting to bytearray for sending
        # Sending assist torque request to assist motor
        s10 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s10.connect((TCP_IP,TCP_PORT25))
        s10.send(assist_send)
        data = s10.recv(BUFFER_SIZE)
        print(f'sending assist torque data: {list(data)} Nm')
        s10.close()

        time.sleep(1)

        TCP_PORT11 = 5044
        load_send = bytearray([y])  # converting to bytearray for sending
        # Sending load torque request to load motor
        s11 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s11.connect((TCP_IP,TCP_PORT11))
        s11.send(load_send)
        data2 = s11.recv(BUFFER_SIZE)
        print(f'sending load torque data: {list(data2)} Nm')
        s11.close()


        TCP_PORT2 = 5003

        # Sending load torque request to load motor
        from can import Message
        # Here can_msg is the CAN frame to be sent as 3 payloads
        can_msg = Message(is_extended_id=False,arbitration_id=1,data=[2])
        print(can_msg)  # printing CAN frame
        # converting is_extended_id to sent via socket
        bool_val = can_msg.is_extended_id
        # Converting boolean to integer
        if bool_val :
            bool_val = 1
        else :
            bool_val = 0
        Payload1 = [bool_val]
        Payload2 = [can_msg.arbitration_id]
        Payload3 = list(can_msg.data)
        msg_array = Payload1 + Payload2 + Payload3
        Payload = bytearray(msg_array)


        # Sending the CAN frame to CAN simulator via socket

        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.connect((TCP_IP,TCP_PORT2))
        print(f"Connecting sender socket with port {TCP_PORT2}")
        s2.send(Payload)
        data3 = s2.recv(BUFFER_SIZE)
        print(f'sending gateway data: {list(data3)} Nm')
        s2.close()
        print("-----------------------------------------------------------------")

    def rtc(self,x):
        TCP_IP = "0.0.0.0"  # IP of laptop
        BUFFER_SIZE = 1024

        TCP_PORT = 5025
        assist_send = bytearray([0,x])  # converting to bytearray for sending
        # Sending assist torque request to assist motor
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((TCP_IP,TCP_PORT))
        s.send(assist_send)
        data = s.recv(BUFFER_SIZE)
        print(f'sending assist torque for RTC: {list(data)} Nm')
        s.close()

        TCP_PORT2 = 5003

        # Sending load torque request to load motor
        from can import Message
        # Here can_msg is the CAN frame to be sent as 3 payloads
        can_msg = Message(is_extended_id=False,arbitration_id=1,data=[3])
        print(can_msg)  # printing CAN frame
        # converting is_extended_id to sent via socket
        bool_val = can_msg.is_extended_id
        # Converting boolean to integer
        if bool_val :
            bool_val = 1
        else :
            bool_val = 0
        Payload1 = [bool_val]
        Payload2 = [can_msg.arbitration_id]
        Payload3 = list(can_msg.data)
        msg_array = Payload1 + Payload2 + Payload3
        Payload = bytearray(msg_array)

        # Sending the CAN frame to CAN simulator via socket

        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.connect((TCP_IP,TCP_PORT2))
        print(f"Connecting sender socket with port {TCP_PORT2}")
        s2.send(Payload)
        data3 = s2.recv(BUFFER_SIZE)
        print(f'sending gateway data: {list(data3)} Nm')
        s2.close()
        print("-----------------------------------------------------------------")

    def run(self):
        # Receive Angle and torque
        angle = np.load('angle.npy')  # load
        steering_torque = np.load('steering_torque.npy')  # load

        # Receive Vehicle Speed from ABS via CANBus
        global myarray
        receiving_completed_flag = 0
        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response
        print('\n')
        print('Starting a new connection')
        packet = self.conn.recv(BUFFER_SIZE1)

        can_id, can_bool, vehicle_speed = self.dissect_can_frame(packet)
        log.debug('Received: can_id=%x, can_bool=%x, Vehicle Speed=%s', can_id, can_bool, vehicle_speed)
        arbitration_id = can_id
        # print(f"arbitration id before passing on is {arbitration_id}")
        lock.acquire()
        myarray = packet      # Add packet elements       # working but override
        print("Closing receiver socket")
        # print(f'final array of vehicle speed is {myarray}')
        self.conn.close()
        # print("Out of receiver for loop")
        receiving_completed_flag = 1
        # print(f'current value of receiving_completed_flag is {receiving_completed_flag}')
        lock.release()

        # Sender socket of EPS as per Rafiul's code
        torque_constant1 = 20  # for low speed
        torque_constant2 = 10  # for high speed


        if receiving_completed_flag == 1:
            #  EPS process for right turn torque calculation
            if angle > 0 and 0 <= vehicle_speed[0] < 25 and steering_torque > 0:
                assist_torque = torque_constant1 - steering_torque
                load_torque = assist_torque + steering_torque
                print("Calculating assist torque at low speed: %s Nm" % assist_torque)
                print("Calculating load torque at low speed: %s Nm" % load_torque)
                self.torque_send(assist_torque, load_torque)

            elif angle > 0 and vehicle_speed[0] >= 25 and steering_torque > 0:
                assist_torque = torque_constant2 - steering_torque
                load_torque = assist_torque + steering_torque
                print("Calculating assist torque at high speed: %s Nm" % assist_torque)
                print("Calculating load torque at high speed: %s Nm" % load_torque)
                self.torque_send(assist_torque, load_torque)
            elif angle > 0 and 5 < vehicle_speed[0] < 25 and steering_torque < 1:
                assist_torque = 20
                self.rtc(assist_torque)
                print("RTC state activated")
            else:
                print("Right turn not applied")
                print("Sending no data to assist motor and load motor")

        return arbitration_id, can_bool, vehicle_speed


    # ------------------------------------------------------------

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


def main():

    print("Starting EPS process")

    # Creating receiver socket first to get vehicle speed and call function(having sender socket) inside it
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5061			# It has arbitration ID 6 in dictionary

    ClientCount = 0
    myarray = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    log.info('Created a socket')

    # Listener/Receiver section
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:         # This is to make receiver from one socket and sender to other socket in 1 loop

        conn, addr = s.accept()
        conn.setblocking(0)
        thread1 = Dual_thread(conn)
        thread1.start()

if __name__ == '__main__':
    threading.Thread(target=main).start()
    threading.Thread(target=eps_recv).start()



















