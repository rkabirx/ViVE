# This program generates and sends vehicle speed value as part of CAN frame from ADAS to CAN simulator

def adas(x) :
    import socket
    import time

    TCP_IP = "0.0.0.0"
    TCP_PORT = 5003  # port for 1st payload (is_extended_id)
    BUFFER_SIZE = 1024

    print("Starting ADAS process for vehicle speed")

    # Generating simulated vehicle speed value from ADAS
    array1 = list(range(5,30,5))
    array2 = list(range(30,4,-5))
    # Pressed brake at speed 20mph on icy road and ADAS calculating expected speed
    vehicle_speed = array1 + array2
    print(vehicle_speed)

    from can import Message
    # Here can_msg is the CAN frame to be sent as 3 payloads
    can_msg = Message(is_extended_id=False,arbitration_id=x,data=vehicle_speed)

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
        try:
            for x in vehicle_speed :
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                MESSAGE = bytearray([bool_val,can_msg.arbitration_id,x])
                s.send(MESSAGE)
                print("Sending vehicle speed",list(MESSAGE))
                data1 = s.recv(BUFFER_SIZE)
                time.sleep(5)
                s.close()
        except:
            socket.error

if __name__ == '__main__' :
    adas()
