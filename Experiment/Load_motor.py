# Accepts value from EPS to provide Load torque to driver

import socket
from tkinter import *

TCP_IP = "0.0.0.0"
TCP_PORT = 5044
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

while True:
    # socket connection
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)


    conn, addr = s.accept()

    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        load_torque = list(data)[0]
        if load_torque == 0:
            print("Load torque disabled")
        else:
            print("Apply load torque %s Nm to rack & pinion" % load_torque)
        conn.send(data)  # echo
    conn.close()

    def print_output() :
        # if you want the button to disappear:
        # button.destroy() or button.pack_forget()
        label = Label(root,text=("Apply %s Nm to rack&pinion" % load_torque))
        label.config(width=32,font=("Courier",16))
        # this creates x as a new label to the GUI
        label.pack()

    root = Tk()
    root.after(3000,lambda : root.destroy())
    button = Button(root,command=print_output)
    button.pack()

    print_output()
    root.mainloop()

