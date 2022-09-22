# Receives instruction from CAN simulator regarding engine torque
import socket
from tkinter import *


def ECM():
	TCP_IP = "0.0.0.0"
	TCP_PORT5 = 5065
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response

	while True:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((TCP_IP,TCP_PORT5))
		s.listen(1)

		conn, addr = s.accept()
		print("Connected by: ", addr)
		while 1:
			data = conn.recv(BUFFER_SIZE)
			if not data:
				break
			datalist = list(data)
			conn.send(data)  # echo
		
		conn.close()

		from can import Message  # importing CAN frame using python-can library
		# can_msg is the assembled CAN frame with received payloads
		can_msg = Message(is_extended_id=bool(datalist[0]),arbitration_id=datalist[1],data=datalist[2:])
		print("Assembled CAN frame: ", can_msg)

		torque_reduction = datalist[2]

		print("Reduce engine torque by %s unit for traction control" % datalist[2])

		def print_output():
			# if you want the button to disappear:
			# button.destroy() or button.pack_forget()
			label = Label(root,text=("Reduce engine torque by %s unit" % datalist[2]))
			label.config(width=32,font=("Courier",16))
			# this creates x as a new label to the GUI
			label.pack()


		root = Tk()
		root.after(3000,lambda : root.destroy())
		button = Button(root,command=print_output)
		button.pack()

		print_output()
		root.mainloop()


if __name__ == '__main__':
	ECM()
