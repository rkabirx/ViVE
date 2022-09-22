# Accepts value from EPS to provide Assist torque to driver


import socket
from tkinter import *

TCP_IP = "0.0.0.0"
TCP_PORT25 = 5025

BUFFER_SIZE = 20  # Normally 1024, but we want fast response

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT25))
    s.listen(1)

    conn, addr = s.accept()

    print("Socket connection established")

    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        assist_torque = list(data) # the 2nd value of the array is assist torque
        if len(assist_torque) == 1:
            print("Apply %s Nm to steering wheel" % assist_torque[0])
        else:
            print("Apply %s Nm for RTC" % assist_torque[1])
        conn.send(data)  # echo
    conn.close()

    def print_output() :
        # if you want the button to disappear:
        # button.destroy() or button.pack_forget()
        if len(assist_torque) == 1 :
            label = Label(root,text=("Apply %s Nm to steering wheel" % assist_torque[0]))
            label.config(width=32,font=("Courier",16))
        else:
            label = Label(root,text=("Apply %s Nm for RTC" % assist_torque[1]))
            label.config(width=32,font=("Courier",16))
        # this creates x as a new label to the GUI
        label.pack()

    root = Tk()
    root.after(3000,lambda : root.destroy())
    button = Button(root,command=print_output)
    button.pack()

    print_output()
    root.mainloop()



