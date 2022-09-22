import socket
from tkinter import *
from tkinter.ttk import *
import numpy as np
from time import strftime
# from Arduino_Data import *


# def Get_Baud_Rate():
#     mylabel = Label(root, text=B_Rate.get())
#     mylabel.pack()
# 

def Choose_Sensor(event):
    mylabel = Label(root, text=SensorChosen.get()).pack()


def Sensor_Status(event):
    mylabel = Label(root, text=SensorStatus.get()).pack()


# This will collect the text from the text entry box
def click():
    textentry = Entry(root, width=20)
    entered_text = textentry.get()


# def Trigger_Attack():     # To be called for Attack button

## Call function in Arduino_Data.py to start or stop victim car and plot graph for 30 distance values


def No_Attack():
    Get_Sensor_Data(Baud_Rate)


# creating tkinter window
root = Tk()
root.title('Attack Platform')
# root.configure(background = "black")
# Creating Menubar
menubar = Menu(root)

# Adding Attack Menu and commands
attack = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Types of Attack', menu=attack)
# attack.add_command(label='Sensor Attack', command=Sensor_Attack)


##### Victim Information
# ----------------------------------------------------------------------------
# Add text
Text_Baud = Label(root,
                  text="Type of Victim Sensor: HC-SR04 with Baud Rate = 9600\n")  # ,bg="black", fg="white", font="none 12 bold").grid(row=1, column=0, sticky=W)
Text_Baud.pack()

# ----------------------------------------------------------------------------

##### Ask learner to input type of sensor for attack
# ----------------------------------------------------------------------------
# Add text
Text_Baud = Label(root, text="Please select the type of Sensor for attack:")
Text_Baud.pack()

# Select Attacker Sensor type from drop down
# Temp_Variable = StringVar()
options = ('URM37',
           'HC-SR04',
           'SRF05',
           'Parallax PING')
# SensorChosen.grid(column= 1, row= 3)
SensorChosen = Combobox(root, width=50, value=options)
SensorChosen.current()
SensorChosen.bind("<<Comboboxselected>>", Choose_Sensor)
SensorChosen.pack()
# ----------------------------------------------------------------------------

##### Ask learner to input Baud Rate
# ----------------------------------------------------------------------------
# Add text
# Baud_Rate = 9600


def printtext():
    global Box_Baud
    global Baud_Rate
    Baud_Rate = Box_Baud.get()
    text.insert(INSERT, Baud_Rate)
    # the variable user_input saves the baud-rate entered by the user

    np.save('baud_rate.npy' , Baud_Rate)  # save
    print(f"Baud Rate received from user is {Baud_Rate}")


Text_Baud = Label(root, text="Baud Rate for Victim Sensor is:")
Text_Baud.pack()

Box_Baud = Entry(root, width=50)
Box_Baud.pack()
Box_Baud.focus_set()

text = Text(root)

b = Button(root,text='okay',command=printtext)
text.pack()
b.pack(side='bottom')
text.pack()

root.mainloop()

# content = StringVar()
# # Change Attacker Sensor baud rate
# Box_Baud = Entry(root, textvariable= content, width = 50)
# Box_Baud.pack()
#
# Baud_Rate= Box_Baud.get()
# My_Rate = Label(root, text=Baud_Rate)
# My_Rate.pack()



# ----------------------------------------------------------------------------
##### Ask learner to input type of sensor for attack
# ----------------------------------------------------------------------------
# Add text
Text_Baud = Label(root, text="Sensor Status:")
Text_Baud.pack()

# Select Attacker Sensor type from drop down
# Temp_Variable = StringVar()
options2 = ('ON',
            'OFF')
# SensorChosen.grid(column= 1, row= 3)
SensorStatus = Combobox(root, width=50, value=options2)
SensorStatus.current()
SensorStatus.bind("<<Combobox2selected>>", Sensor_Status)
SensorStatus.pack()
# ----------------------------------------------------------------------------

# No attack button
B2 = Button(root, text="No Attack", width=20, command=No_Attack)  #
B2.pack()

# Attack button      # To trigger the start of the attack if baud rate is 9600 and sensor is on
B1 = Button(root, text="Attack Now", width=20,
            command=click)  # Need to call Trigger_Attack() function to start Attacker sensor
B1.pack()

# Exit button
B2 = Button(root, text="Exit", width=20, command=click)  # .grid(row=2, column=0, sticky=W)
B2.pack()

# display Menu
root.config(menu=menubar)
mainloop()

# def Print_Arduino_Info():
#     label = Label(root, text= "Connect Ultrasonic Sensor to Arduino with Echo Pin = 13 and Trig Pin = 10")
#     #label2 = Label(root, text= "Connect Raspberry Pi of Victim Car to Arduino to provide Sensor data to RPI")
#     #label3 = Label(root, text= "Verify and Upload .ino code to Arduino using Arduino IDE in RPI desktop")
#     label.config(width=50, font=("Courier", 24))
#     label.pack()
# 
# # def Print_Arduino_Info():
# #     print("Connect Ultrasonic Sensor to Arduino with Echo Pin = 13 and Trig Pin = 10")
# 
# def Get_Baud_Rate():
#     mylabel = Label(root, text=B_Rate.get())
#     mylabel.pack()
# 
# def Sensor_Attack(Baud_Rate):
#     ## Connect Arduino with Sensor and RPI manually
#     # Print instructions in pop up screen
#     button = Button(root, command= Print_Arduino_Info)
#     button.pack()
#     Print_Arduino_Info()
#     
#     Get_Sensor_Data(Baud_Rate)      # Call function in Arduino_Data.py to start or stop victim car and plot graph for 30 distance values
#     
# 
# # creating tkinter window
# root = Tk()
# root.title('Attack Platform')
# root.configure(background = "black")
# # Creating Menubar
# menubar = Menu(root)
# 
# # Adding Instruction Menu and commands
# instruction = Menu(menubar, tearoff=0)
# menubar.add_cascade(label='Instruction', menu=instruction)
# #instruction.add_command(label='Sensor_info', command=sensor)
# 
# instruction.add_separator()
# instruction.add_command(label='Exit', command=destroy)
# 
# # Change Victim Sensor values
# B_Rate = Entry(root, width=50)
# B_Rate.pack()
#     
# attack = Menu(menubar, tearoff=0)
# menubar.add_cascade(label='Sensor Configuration', menu=attack)
# attack.add_command(label='Baud Rate', command=Get_Baud_Rate)
# 
# # Adding Attack Menu and commands
# attack = Menu(menubar, tearoff=0)
# menubar.add_cascade(label='Types of Attack', menu=attack)
# attack.add_command(label='Sensor Attack', command=Sensor_Attack)
# 
# 
# # display Menu
# root.config(menu=menubar)
# mainloop()
