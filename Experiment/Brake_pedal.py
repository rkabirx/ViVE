# Brake pedal to apply brakes
# Sends brake pedal position status as binary value to BCM ECU


def brake_send(port):

    import tkinter as tk  # import GUI
    import socket
    import time
    import numpy as np

    TCP_IP = "0.0.0.0"  # IP of RPI1
    TCP_PORT = port

    BUFFER_SIZE = 1024


    def brake_OFF():
        MESSAGE = bytearray([0, 0])  # sending 0 to denote TCS OFF

        # Sending to TCS via socket
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending No brake signal")
            data = s.recv(BUFFER_SIZE)
            s.close()
            # root.after(2000,lambda: root.destroy())
        except:
            socket.error

    brake_OFF()

    def brake_ON():
        MESSAGE = bytearray([0, 1])  # sending 0 to denote TCS OFF

        # Sending to TCS via socket
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((TCP_IP,TCP_PORT))
            s.send(MESSAGE)
            print("Sending brake signal")

            data = s.recv(BUFFER_SIZE)
            s.close()
        except:
            socket.error

    def random_brake():
        random_value = np.random.randint(2,size=10)
        for x in random_value :
            MESSAGE = bytearray([0,x])
            # Sending to TCS via socket
            try:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((TCP_IP,TCP_PORT))
                s.send(MESSAGE)
                print("Sending brake signal: ",x)

                data = s.recv(BUFFER_SIZE)
                s.close()
                time.sleep(5)
            except:
                socket.error


    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    OFF = tk.Button(frame,
                    text="No brake",
                    fg="red",
                    command=brake_OFF)
    OFF.pack(side=tk.LEFT)
    ON = tk.Button(frame,
                   text="Brake apply",
                   fg="green",
                   command=brake_ON)
    ON.pack(side=tk.LEFT)
    random = tk.Button(frame,
                   text="Auto random brake",
                   fg="blue",
                   command=random_brake)
    random.pack(side=tk.RIGHT)
    root.mainloop()


if __name__ == '__main__':
    brake_send()
