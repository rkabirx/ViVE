# TCS button to switch ON or OFF the TCS function
# Send ON/OFF status as binary value to TCS ECU

def tcs():
    import tkinter as tk
    import socket
    import time
    import sys
    import numpy as np

    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT = 6001

    BUFFER_SIZE = 1024

    def TCS2(x) :

        TCP_PORT2 = 6002

        BUFFER_SIZE = 1024
        # binary 0 represents no acceleration.
        # binary 1 represents acceleration applied.

        MESSAGE = bytearray([x])
        print("Sending TCS status")
        # Sending to ABS RPI2 via socket
        try:
            s3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s3.connect((TCP_IP,TCP_PORT2))
            s3.send(MESSAGE)
            data3 = s3.recv(BUFFER_SIZE)
            s3.close()
            time.sleep(2)
        except:
            socket.error

    def TCS_ON():
        MESSAGE = bytearray([0, 1])  # sending 0 to denote TCS OFF

        # Sending to TCS via socket
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending TCS status to Instrument cluster")
            data = s.recv(BUFFER_SIZE)
            s.close()
            TCS2(1)
        except:
            socket.error


    TCS_ON()

    def TCS_OFF():
        MESSAGE = bytearray([0, 0])  # sending 0 to denote TCS OFF

        # Sending to TCS via socket
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending TCS status to Instrument cluster")
            data = s.recv(BUFFER_SIZE)
            s.close()
            TCS2(0)
        except:
            socket.error


    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    OFF = tk.Button(frame,
                    text="TCS OFF",
                    fg="red",
                    command=TCS_OFF)
    OFF.pack(side=tk.RIGHT)
    ON = tk.Button(frame,
                   text="TCS ON",
                   fg="green",
                   command=TCS_ON)
    ON.pack(side=tk.RIGHT)

    root.mainloop()


if __name__ == '__main__':
    tcs()






