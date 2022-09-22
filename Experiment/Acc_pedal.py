# Accelerator pedal to apply acceleration
# Sends accelerator pedal position status as binary value

def acc_pedal(port) :
    import tkinter as tk
    import socket
    import time
    import numpy as np

    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT = port

    BUFFER_SIZE = 1024

    def acc_OFF():

        MESSAGE = bytearray([0,0,0])  # sending 0 to denote TCS OFF
        try:
            # Sending to TCS via socket
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending No acceleration signal")
            data = s.recv(BUFFER_SIZE)
            s.close()

        except:
            socket.error

    acc_OFF()

    def acc_ON() :
        MESSAGE = bytearray([0,0,1])  # sending 0 to denote TCS OFF
        try:
            # Sending to TCS via socket
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending acceleration signal")
            data = s.recv(BUFFER_SIZE)
            s.close()

        except:
            socket.error

    def random_press():
        random_value = np.random.randint(2, size=10)
        for x in random_value:
            MESSAGE = bytearray([0,0,x])  # sending 0 to denote TCS OFF
            try :
                # Sending to TCS via socket
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                s.send(MESSAGE)
                print("Sending automatic random acc signal: ",x)
                data = s.recv(BUFFER_SIZE)
                s.close()
                time.sleep(5)
            except :
                socket.error

    while True:
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()

        OFF = tk.Button(frame,
                        text="No acceleration",
                        fg="red",
                        command=acc_OFF)
        OFF.pack(side=tk.LEFT)
        ON = tk.Button(frame,
                       text="Accelerate",
                       fg="green",
                       command=acc_ON)
        ON.pack(side=tk.LEFT)
        random = tk.Button(frame,
                       text="Auto random generate",
                       fg="blue",
                       command=random_press)
        random.pack(side=tk.RIGHT)
        root.mainloop()


if __name__ == '__main__' :
    acc_pedal()
