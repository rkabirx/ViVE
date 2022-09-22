# Simulated torque sensor value send to EPS


def send_torque():
    import socket
    import time

    # TCP_IP = "192.168.0.8"  # IP of RPI1
    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT3 = 5004

    BUFFER_SIZE = 1024
    Torque_array = [0, 2, 3, 4, 0]  # torque provided by driver to make right turn

    while True:

        for x in Torque_array:

            # Sending toque to EPS RPI2 via socket
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT3))
            MESSAGE = bytearray([0, x])
            s.send(MESSAGE)
            print("Sending torque",list(MESSAGE))
            data = s.recv(BUFFER_SIZE)
            time.sleep(5)
            s.close()



if __name__ == '__main__':
    send_torque()
