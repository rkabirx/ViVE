
# This program generates simulated wheel speed sensor value and sends to RPI2 (ABS) via socket


import socket
import time

TCP_IP = "0.0.0.0"  # IP of RPI1
TCP_PORT = 5093

BUFFER_SIZE = 1024

# lets consider a situation where
tire1_diameter = 15
tire2_diameter = 14
tire3_diameter = 11
tire4_diameter = 15

tire_diameters = [tire1_diameter,tire2_diameter,tire3_diameter,tire4_diameter]


while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    MESSAGE = bytearray(tire_diameters)  # sending 1 to denote acceleration applied
    print("Sending Tire diameters: ",tire_diameters)
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    time.sleep(3)
    s.close()
