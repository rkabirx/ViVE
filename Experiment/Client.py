import socket
import time

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 5010))
    message = bytearray([1])
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    time.sleep(3)
    print ('Received', repr(data))