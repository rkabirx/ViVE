
def send(port):
    import socket
    import time
    import sys
    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT1 = port  # goes to ABS

    BUFFER_SIZE = 1024

    # Generating simulated wheel speed sensor value
    array1 = list(range(5,30,5))
    array2 = list(range(30,4,-5))
    # Pressed brake at speed 20mph on icy road and wheel speed sensor giving 0 mph

    wheel_speed = array1 + array2
    while True :
        try:
            for x in wheel_speed :
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT1))
                MESSAGE = bytearray([x])
                s.send(MESSAGE)
                print("Sending wheel speed",list(MESSAGE))
                data = s.recv(BUFFER_SIZE)
                # print("Client received data: ",data)
                time.sleep(5)
                s.close()
        except:
            socket.error


if __name__ == '__main__' :
    send()