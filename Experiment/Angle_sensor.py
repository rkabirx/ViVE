# Simulated angle sensor value send to EPS

def send_angle():
    import socket
    import time
    # TCP_IP = "192.168.0.8"  # IP of RPI1
    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT2 = 5004

    BUFFER_SIZE = 1024
    Angle_array = [0, 45, 90, 135, 180]

    # Sending angle to EPS RPI2 via socket

    while True:

        for x in Angle_array:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT2))
            MESSAGE = bytearray([x])
            s.send(MESSAGE)
            print("Sending angle",list(MESSAGE))
            data = s.recv(BUFFER_SIZE)
            time.sleep(5)
            s.close()


if __name__ == '__main__':
    send_angle()
