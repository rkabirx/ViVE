import socket
from tkinter import *
from tkinter.ttk import *
from time import strftime

TCP_IP = "0.0.0.0"  # IP of arduino
TCP_PORT = 5005

def sensor():
    print("Find the ultrasound sensor signature of target car")

def car ():
    print("Honda Accord 2010")

def send():
    MESSAGE = bytearray([1])  # sending 0 to denote TCS OFF

    # Sending to TCS via socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print("Sending signal")

        data = s.recv(1024)
        s.close()
    except:
        socket.error

def stop():
    MESSAGE = bytearray([0])  # sending 0 to denote TCS OFF

    # Sending to TCS via socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print("Sending signal to stop")

        data = s.recv(1024)
        s.close()
    except:
        socket.error

# creating tkinter window
root = Tk()
root.title('Menu Demonstration')

# Creating Menubar
menubar = Menu(root)

# Adding Instruction Menu and commands
instruction = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Instruction', menu=instruction)
instruction.add_command(label='Sensor_info', command=sensor)
instruction.add_command(label='Car_info', command=car)

instruction.add_separator()
instruction.add_command(label='Exit', command=root.destroy)

# Adding Attack Menu and commands
attack = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Attack', menu=attack)
attack.add_command(label='Send signal', command=send)
attack.add_command(label='Stop signal', command=stop)



# display Menu
root.config(menu=menubar)
mainloop()