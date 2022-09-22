import socket
from tkinter import *
from tkinter.ttk import *
from time import *
from tkinter.messagebox import *
import _thread
from multiprocessing import Process
import threading
import subprocess
from multiprocessing import Process

from CANBus_Congestion import *
from CANBus_Latency import *
from Gateway import *
# from ABS_servers import ABS_Servers_Main
from RT_servers import RT_Servers_Main
from TCS_servers import TCS_Servers_Main
from ABS_Clients import ABS_Clients_Main
from RT_Clients import RT_Clients_Main
from TCS_Clients import TCS_Clients_Main
import WheelSpeed_sensor
from ADAS import *
import Brake_pedal
from Hydraulic_modulator import *
from ABS_ECU import *

from Create_Use_Case import *


Stop_Flag = 0
Selected_Use_Cases = 0
Selected_Apply_option = 0
Selected_Opt_Technique = 0
Run_Flag = 0
root = 0
choices = {}
#------------------------------------------------------------------------------------
def Stop_function():
    global Stop_Flag
    Stop_Flag = 1
    # root.after(2000, lambda: showerror("error", "Stopping current functionality"))
    root.after(2000, lambda: showerror("error", "Stopping current functionality"))
    print(f"Stop flag is {Stop_Flag}")
    # root.after(2000, root.destroy)
    #https://stackoverflow.com/questions/31410462/how-to-stop-a-running-function-without-exiting-the-tkinter-window-entirely
    #https://stackoverflow.com/questions/40041440/how-to-stop-or-interrupt-a-function-in-python-3-with-tkinter/46335224
    #https://stackoverflow.com/questions/27319580/after-cancel-usage-as-a-stop-method

def Call_Server_Functions_Of_UseCases(threadName):
    global choices

    Hyd_Mod_PORT = 5010
    CAN_PORT2 = 5003

    print("Starting Server thread")

    if Create_Flag == 1:
        for receiver in Receiver_List:  # Components in the "Output" column in GUI
            # I think I will have to add components of Middle column in this as well as they are also receivers (though sender as well)
            if receiver == 'Hydraulic Modulator':
                p1 = Process(target=Hydraulic_Modulator_Call)
                p1.start()
            # elif receiver == 'ABS ECU':   # Automatically starts
            if receiver == 'Gateway':
                # threading.Thread(target=Gateway_function)
                # Gateway_Thread.start()
                p2 = Process(target=Gateway_function)
                p2.start()


    if "Anti Lock Braking System" in choices:
            print("Running ABS ECU")
            # subprocess.run("python3 ABS_servers.py", shell=True)
            p1 = Process(target=ABS_ECU_Run_Threads, args=(Hyd_Mod_PORT, CAN_PORT2, ))
            p1.start()

            p1 = Process(target=Hydraulic_Modulator_Call)
            p1.start()

        # elif "Traction Control System" in choices:
        #     print("Running TCS Servers")
        #     subprocess.run("python3 TCS_servers.py", shell=True)
        #
        # elif "Right Turn and Return to Centre" in choices:
        #     print("Running RT+RTC Servers")
        #     subprocess.run("python3 RT_servers.py", shell=True)

def WheelSpeed_Call(temp_port1) :
    WheelSpeed_sensor.send(temp_port1) # In this way, can change port numbers for different use cases

def ADAS_Call(temp_port2) :
    adas(6, temp_port2)  # In this way, can change arb id for different use cases

def Brake_pedal_Call() :
    Brake_pedal.brake_send(5005)

def Hydraulic_Modulator_Call() :
    Hydraulic_Modulator_Main()

def Gateway_function():
    Gateway_Main()

def Call_Client_Functions_Of_UseCases(threadName):
    print("Starting Client thread")
    if Create_Flag == 1:
        for sender in Connection_Port_Dictionary.keys():
            if sender == 'Wheel Speed Sensor':
                temp_port1 = Connection_Port_Dictionary[sender]
                print("Wheel speed connects to", temp_port1)
                p1 = Process(target=WheelSpeed_Call, args=(temp_port1, ))
                print("Starting Wheel speed sensor")
                p1.start()
            elif sender == 'ADAS ECU':
                temp_port2 = Connection_Port_Dictionary[sender]
                print("ADAS connects to", temp_port2)
                p2 = Process(target=ADAS_Call, args=(temp_port2, ))
                print("Starting ADAS")
                p2.start()
            elif sender == 'Brake Pedal Sensor':
                temp_port3 = Connection_Port_Dictionary[sender]
                print("Brake Pedal connects to", temp_port3)
                p3 = Process(target=Brake_pedal_Call, args=(temp_port3, ))
                print("Starting Brake Pedal sensor")
                p3.start()
            elif sender == 'ABS ECU':
                temp_port4 = Connection_Port_Dictionary[sender]
                Output1_Port = temp_port4[0]        # Making it static as ABS has two ouput ports for ABS ECU - Need to change it
                Output2_Port = temp_port4[1]

                print("ADAS connects to", temp_port4)
                print("Starting ABS ECU with Ports", Output1_Port, Output2_Port)
                p1 = Process(target=ABS_ECU_Run_Threads, args=(Output1_Port, Output2_Port, ))
                p1.start()

            else:
                print("Error: Sender not in the known list")
            ## Only added as per ABS use case...need to add rest of the senders if condition


    if "Anti Lock Braking System" in choices:
        print("Running ABS Clients")
        # subprocess.run("python3 ABS_Clients.py", shell=True)
        print("----------------------------------------In ABS_Clients.py------------------------------------------")
        p1 = Process(target=WheelSpeed_Call)
        print("Starting Wheel speed sensor")
        p1.start()
        p2 = Process(target=ADAS_Call)
        print("Starting ADAS")
        p2.start()
        p3 = Process(target=Brake_pedal_Call)
        print("Starting Brake Pedal sensor")
        p3.start()

    # elif "Traction Control System" in choices:
    #     print("Running TCS Clients")
    #     subprocess.run("python3 TCS_Clients.py", shell=True)
    #
    # elif "Right Turn and Return to Centre" in choices:
    #     print("Running RT+RTC Clients")
    #     subprocess.run("python3 RT_Clients.py", shell=True)

def Start_CAN_Bus(threadName, Current_Selected_Apply_option, Current_Selected_Opt_Technique):
    try:
        print("Starting CAN bus thread from GUI")
        if Current_Selected_Apply_option == 'Yes':
            if Current_Selected_Opt_Technique == 'Simulated Annealing - For Congestion':
                print("Running congestion and servers")
                subprocess.run("python3 CANBus_Congestion.py", shell=True)

            elif Current_Selected_Opt_Technique == 'Simulated Annealing - For Latency':
                print("Running Latency")
                subprocess.run("python3 CANBus_Latency.py", shell=True)

            else:   # None case
                showerror("error", "You need to select a technique")

        elif Current_Selected_Apply_option == 'No':       # No optimization case
            print("Run use cases without optimization function")

        else:
            print("You have not answers for all questions")

    except Exception:
        import traceback
        print(traceback.format_exc())



def Run_Use_cases():
    try:
        global Stop_Flag
        global Selected_Use_Cases
        global Selected_Apply_option
        global Selected_Opt_Technique
        global root
        global choices
        global Run_Flag

        Run_Flag = 1

        print(f"Selected use cases visible in Run_Use_case function are {Selected_Use_Cases}")

        print("Connection_Port_Dictionary is in main function as ", Connection_Port_Dictionary)

        ## Get all the selected options first
        Current_Selected_Apply_option = Selected_Apply_option.get()
        print(f"Current_Selected_Apply_option is {Current_Selected_Apply_option}")

        Current_Selected_Opt_Technique = Selected_Opt_Technique.get()
        print(f"Current Selected_Opt_Technique is {Current_Selected_Opt_Technique}")

        threadLock = threading.Lock()
        # Create new threads
        CAN_Thread = threading.Thread(target=Start_CAN_Bus, args=("CAN Thread", Current_Selected_Apply_option, Current_Selected_Opt_Technique, ))
        # Gateway_Thread = threading.Thread(target=Gateway_function)

        ## Start server and client for every selected use case
        Server_Thread = threading.Thread(target=Call_Server_Functions_Of_UseCases, args=("Server Thread", ))
        Client_Thread = threading.Thread(target=Call_Client_Functions_Of_UseCases, args=("Client Thread", ))

        # Start new Threads
        # Gateway_Thread.start()
        CAN_Thread.start()
        Server_Thread.start()
        Client_Thread.start()

        # if Stop_Flag == 1:
        #     root.after(2000, lambda: showerror("error", "Stopping current functionality"))
        #     Stop_Flag = 0

        # root.after(500, scanning)

    except KeyboardInterrupt:
        exit()

# def scanning():
#     global Stop_Flag
#     global Attack_Flag
#
#     #print(f"In scanning function: Stop flag is {Stop_Flag}")
#
#     if Stop_Flag !=1:
#         #print("In scanning if condition")
#         Get_Sensor_Data(Baud_Rate, Attack_Flag)
#
#     root.after(500, scanning)

class Select_UseCases(Frame):
    global root
    global choices

    def __init__(self, parent, **kw):
        Frame.__init__(self, parent)
        self.choices = choices
        # attack = Menu(menubar, tearoff=0)
        # menubar.add_cascade(label='Run Use Cases', menu=attack)
        super().__init__(**kw)
        menubutton = Menubutton(self, text="Choose Use cases") #indicatoron=True, borderwidth=1, relief="raised"
        menu = Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        menubutton.pack(padx=10, pady=10)

        #choices = {}
        for choice in ("Anti Lock Braking System", "Traction Control System", "Right Turn and Return to Centre", "Cruise Control", "Tire Pressure Monitoring System"):
            self.choices[choice] = IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=self.choices[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.printValues)
        #print(f"Selected use case is {self.choices}")

    def printValues(self):
        for name, var in choices.items():
            print("%s: %s" % (name, var.get()))

#### Main function ----------------------------------------------------------------------------
def main():
    global choices
    global Selected_Apply_option
    global Selected_Opt_Technique
    global Selected_Use_Cases
    global root

    # creating tkinter window
    root = Tk()
    root.title('Virtual Platform')
    # Creating Menubar
    menubar = Menu(root)

    # Adding Menu and commands
    attack = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Run Use Cases', menu=attack)

    #----------------------------------------------------------------------------
    ##### User will select the use cases that needs to be run

    # Add text
    Text_Baud = Label(root, text = "Please select all the use cases that you want to execute: ")
    Text_Baud.pack()

    Select_UseCases(root).pack(fill="both", expand=True)
    #----------------------------------------------------------------------------
    ##### Ask user if they want to apply optimization technique

    # Add text
    Text_Baud = Label(root, text = "Apply optimization technique?")
    Text_Baud.pack()

    Temp_apply = StringVar(value="Select")
    options2 = ('Yes',
                'No')

    # Combobox(root, width = 50, state='readonly', value=options2, textvariable= Selected_Apply_option).pack()
    Selected_Apply_option = Combobox(root, width = 50, state='readonly', value=options2)

    Selected_Apply_option.current()
    Selected_Apply_option.bind("<<Combobox2selected>>", Selected_Apply_option)
    Selected_Apply_option.pack()

    # #Error if different status
    # Selected_Apply_option = Temp_apply.get()
    # print(f"Selected Apply option is {Selected_Apply_option}")
    #----------------------------------------------------------------------------
    ##### Ask user which optimization technique should be applied

    Text_Baud = Label(root, text = "Which optimization technique?")
    Text_Baud.pack()

    # Select Attacker Sensor type from drop down
    options3 = ('Simulated Annealing - For Congestion',
                'Simulated Annealing - For Latency',
                'None')

    # Combobox(root, width = 50, value=options3, textvariable = Selected_Opt_Technique).pack()
    Selected_Opt_Technique = Combobox(root, width = 50, value=options3)

    Selected_Opt_Technique.current()
    Selected_Opt_Technique.bind("<<Combobox2selected>>", Selected_Opt_Technique)
    Selected_Opt_Technique.pack()
    # Selected_Opt_Technique = Field3.get()
    # print(f"Selected_Opt_Technique is {Selected_Opt_Technique}")
    #----------------------------------------------------------------------------
    # Run button
    # print("Gonna run Run_Use_case function")
    B1 = Button(root, text="Run and Get Results", width = 20, command=Run_Use_cases)        # Need to call Trigger_Attack() function to start Attacker sensor
    B1.pack()

    # Stop button
    B3 = Button(root, text="Stop", width = 20, command=Stop_function)
    B3.pack()

    # Create button
    # print("Gonna run Run_Use_case function")
    B1 = Button(root, text="Create", width = 20, command=Create_Main_Function)        # This should set Create_Flag to 1
    B1.pack()

    # display Menu
    root.config(menu=menubar)
    mainloop()

if __name__ == '__main__':
    main()






