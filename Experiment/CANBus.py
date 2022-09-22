
import multiprocessing
import threading
import socket
import numpy as np
import time


def can_recv1(port1):
    TCP_IP = "0.0.0.0"
    TCP_PORT1 = port1

    from can import Message  # importing CAN frame using python-can library

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT1))
    s.listen(1)
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break
        datalist = list(data)
        print("received data: %s" % datalist)
        conn.send(data)

        # can_msg is the assembled CAN frame with received payloads
        can_msg = Message(is_extended_id=bool(datalist[0]), arbitration_id=datalist[1], data=datalist[2:])
        print("Assembled CAN frame: ", can_msg)
        np.save('payload1.npy', datalist)  # save
    conn.close()

    time.sleep(2)
    TCP_PORT11 = 5010
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, TCP_PORT11))
    print("Sending")
    s2.send(bytearray(datalist))
    data = s2.recv(1024)
    s2.close()

def can_recv2(port2):
    TCP_IP = "0.0.0.0"
    TCP_PORT2 = port2

    from can import Message  # importing CAN frame using python-can library

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT2))
    s.listen(1)
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break
        datalist = list(data)
        print("received data: %s" % datalist)
        conn.send(data)

        # can_msg is the assembled CAN frame with received payloads
        can_msg = Message(is_extended_id=bool(datalist[0]), arbitration_id=datalist[1], data=datalist[2:])
        print("Assembled CAN frame: ", can_msg)
        np.save('payload2.npy', datalist)  # save
    conn.close()

    time.sleep(2)
    TCP_PORT4 = 5011
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, TCP_PORT4))
    print("Sending")
    s2.send(bytearray(datalist))
    data = s2.recv(1024)
    s2.close()


def can_recv3(port3):
    TCP_IP = "0.0.0.0"
    TCP_PORT3 = port3

    from can import Message  # importing CAN frame using python-can library

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT3))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data: break
        datalist = list(data)
        print("received data: %s" % datalist)
        conn.send(data)

        # can_msg is the assembled CAN frame with received payloads
        can_msg = Message(is_extended_id=bool(datalist[0]), arbitration_id=datalist[1], data=datalist[2:])
        print("Assembled CAN frame: ", can_msg)
        np.save('payload3.npy', datalist)  # save
    conn.close()
    time.sleep(2)

    TCP_PORT6 = 5025
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, TCP_PORT6))
    print("Sending")
    s2.send(bytearray(datalist))
    data = s2.recv(1024)
    s2.close()

if __name__ == '__main__':
    threading.Thread(target=can_recv1).start()
    threading.Thread(target=can_recv2).start()
    threading.Thread(target=can_recv3).start()





























