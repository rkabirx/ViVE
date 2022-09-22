


from threading import Thread,Lock

import socket
from tkinter import *

class listener_thread(Thread):

    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global myarray

        BUFFER_SIZE1 = 1024  # Normally 1024, but we want fast response


        print('Starting a new connection')

        packet = self.conn.recv(BUFFER_SIZE1)
        received_array = list(packet)
        print("Closing receiver socket")
        print("Received packet: ", received_array)

        def printSomething() :
            # if you want the button to disappear:
            # button.destroy() or button.pack_forget()
            label = Label(root,text="Anti-lock braking applied")
            label.config(width=30,font=("Courier",24))
            # this creates x as a new label to the GUI
            label.pack()

        root = Tk()
        root.after(3000,lambda : root.destroy())
        button = Button(root,command=printSomething)
        button.pack()

        printSomething()
        root.mainloop()
        self.conn.close()
        print("Out of receiver for loop")
        print("-----------------------------------------------------------------")

def main():
    TCP_IP = "0.0.0.0"
    TCP_PORT = 5010

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    # log.info('Created a socket')
    print(f"Connecting receiver socket with port {TCP_PORT}")
    s.listen(1)
    print("Receiver is waiting for a connection...")

    while True:  # Check if this is right -> This is to make receiver from one socket and sender to other socket in 1 loop

        conn,addr = s.accept()
        conn.setblocking(0)

        thread = listener_thread(conn)
        thread.start()


if __name__ == '__main__':
    main()





























