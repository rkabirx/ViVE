# Receives TCS status

import socket

TCP_IP = "0.0.0.0"
TCP_PORT1 = 6002
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT1))
    s.listen(1)

    conn, addr = s.accept()

    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        datalist = list(data)
        conn.send(data)  # echo
        if len(datalist) == 1:
            if datalist[0] == 1:
                print("TCS ON")
            else :
                print("TCS OFF")
        elif len(datalist) == 3:
            from can import Message  # importing CAN frame using python-can library

            # can_msg is the assembled CAN frame with received payloads
            can_msg = Message(is_extended_id=bool(datalist[0]),arbitration_id=datalist[1],data=datalist[2 :])
            print("Assembled CAN frame: ",can_msg)

            if datalist[2] == 0:
                print("Instrument panel showing Cruise OFF")
            else :
                print("Instrument panel showing Cruise ON")
        else:
            print("No information")

    conn.close()


