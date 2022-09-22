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

    # Current slip rate
    def calculate_SlipRate(self,current_wheel_speed,current_vehicle_speed):
        slip_rate = ((float(current_vehicle_speed) - float(current_wheel_speed)) * 100) / float(current_vehicle_speed)
        return slip_rate

    def run(self):

        # Receive Wheel Speed from Sensor

        brake_abs = np.load('brake_abs.npy')

        if brake_abs > 0:
            Wheel_Speed = 0
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
        import time
        time.sleep(1)
        print("-----------------------------------------------------------------")
        if receiving_completed_flag == 1:
            print("Inside sender function")
            TCP_IP = "0.0.0.0"

            TCP_PORT = 5010  # To connect to Hydraulic_modulator.py  # Port of HCU
            TCP_PORT2 = 5003  # To connect to Gateway

            BUFFER_SIZE = 1024

            if brake_abs > 0:
                Wheel_Speed = 0
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")
            elif (brake_abs == 0) & (Wheel_Speed == data[0]):
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")
            else:
                Wheel_Speed = data[0]
                print('Calculate sliprate from wheel speed %s and vehicle speed %s' % (Wheel_Speed, data[0]))
                SlipRate = self.calculate_SlipRate(Wheel_Speed, data[0])
                print(f"Slip rate is {SlipRate}\n")

            if (SlipRate > 0.3) & (brake_abs) > 0:
                # current_pressure = float(pressure) - 1  # Find out whether ECU passes pressure or Change in Pressure to HCU
                Pressure = 100
                print("As Slip rate is higher, Current pressure after reduction is " + str(Pressure))
                print("Pressure: ",Pressure)
                print("Sending from ABS to HCU")
                # Sending the Pressure data to Central simulator

                PressureByte = Pressure.to_bytes(2,'big')

                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                print(f"Connecting sender socket with port {TCP_PORT}")
                print("Pressure to be sent to HCU is %s" % Pressure)
                # print(f'Sending {myarray}')
                s.send(bytearray(PressureByte))
                s.close()

                from can import Message
                # Here can_msg is the CAN frame to be sent as 3 payloads
                can_msg = Message(is_extended_id=False,arbitration_id=1,data=[Pressure])
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

                print("Sending array: ",msg_array)

                # Sending the CAN frame to CAN simulator via socket

                s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s2.connect((TCP_IP,TCP_PORT2))
                print(f"Connecting sender socket with port {TCP_PORT2}")
                print("Pressure to be sent to CAN Bus is %s" % Pressure)
                s2.send(Payload)
                data1 = s2.recv(BUFFER_SIZE)
                s2.close()
                print("-----------------------------------------------------------------")
            else:
                print("Slip rate in range" )
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
        if len(received_array) == 1:
            np.save('WheelSpeed.npy' , received_array[0])  # save
        else:
            np.save('brake_abs.npy', received_array[1]) # save
        self.conn.close()
        print("Out of receiver for loop")


def abs_recv():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5005

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

def abs_send():
    # This program generates and sends vehicle speed value as part of CAN frame from ABS to CAN simulator in laptop

    import socket
    import time

    TCP_IP = "0.0.0.0"
    TCP_PORT = 5003  # port for 1st payload (is_extended_id)
    BUFFER_SIZE = 1024

    print("Starting ABS process for vehicle speed")

    # Generating simulated vehicle speed value from ADAS
    array1 = list(range(5,30,5))
    array2 = list(range(30,4,-5))
    # Pressed brake at speed 20mph on icy road and ADAS calculating expected speed
    vehicle_speed = array1 + array2
    print(vehicle_speed)

    from can import Message

    # Here can_msg is the CAN frame to be sent as 3 payloads
    can_msg = Message(is_extended_id=False,arbitration_id=7,data=vehicle_speed)

    print(can_msg)  # printing CAN frame

    # converting is_extended_id to sent via socket
    bool_val = can_msg.is_extended_id
    # Converting boolean to integer
    if bool_val :
        bool_val = 1
    else :
        bool_val = 0

    # Sending the CAN frame to CAN simulator via socket

    while True :
        # Sending to ABS RPI2 via socket
        try :
            for x in vehicle_speed :
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                MESSAGE = bytearray([bool_val,can_msg.arbitration_id,x])
                s.send(MESSAGE)
                print("Sending vehicle speed",list(MESSAGE))
                data1 = s.recv(BUFFER_SIZE)
                time.sleep(5)
                s.close()
        except :
            socket.error

def abs():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5060  # It has arbitration ID 6 in dictionary

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
        thread1 = Dual_thread(conn)
        thread1.start()


if __name__ == '__main__':
    threading.Thread(target=abs).start()
    threading.Thread(target=abs_recv).start()