############ Platform_GUI and Create merged and working condition


## Connection Port Array keeps a track of key = Component, value = The port TO which that componet needs to connect with to SEND data
## Receiver List keeps track of the list of components which will receive data from some components (might be a sender too)

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
from tkinter import *
from functools import partial
from tkinter.ttk import *

from CANBus_Congestion import *
from CANBus_Latency import *
from CAN_Bus_No_Optimization import *

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
from ECM import *
from Instrument_cluster import *
from Create_Use_Case import *
from TCS_recv import *
from TCS_process import *
from Acc_pedal import *
from TCS_switch import *


Stop_Flag = 0
Selected_Apply_option = 0
Selected_Opt_Technique = 0
Run_Flag = 0
root = 0
choices = {}
Chosen_Use_Cases = []

#### New use case
Current_Row=1
Connection_Port_Dictionary = {}
Create_Flag = 0
Receiver_List = []
Selected_Components_Array = [[] for i in range(10)]
Default_Component_Port_Dictionary = {'ABS ECU': 5005, 'Gateway': 7400, 'CAN Bus': 5003, 'Hydraulic Modulator': 5010, 'Assist_Motor':5025, 'ECM':5065, 'Instrument Cluster':6002, 'Load Motor': 5044}
local_index = 0
#------------------------------------------------------------------------------------
def Stop_function():
    global Stop_Flag
    Stop_Flag = 1
    # root.after(2000, lambda: showerror("error", "Stopping current functionality"))
    root.after(2000, lambda: showerror("error", "Stopping current functionality"))
    print(f"Stop flag is {Stop_Flag}")

def WheelSpeed_Call(temp_port1) :
    WheelSpeed_sensor.send(temp_port1) # In this way, can change port numbers for different use cases

def ADAS_Call(temp_port21, temp_port22) :
    adas(temp_port21, temp_port22)  # In this way, can change arb id for different use cases

def Brake_pedal_Call(temp_port3) :
    Brake_pedal.brake_send(temp_port3)

def Hydraulic_Modulator_Call() :
    Hydraulic_Modulator_Main()

def Gateway_function():
    Gateway_Main()

def ECM_Call():
    ECM()

def Instrument_Cluster_Call():
    Instrument()

# def TCS_ECU_Call(Output_Port):
#     print("Starting TCS ECU receiver")
#     p1 = Process(target=tcs_recv)       # In TCS_recv.py
#     p1.start()
#
#     print("Starting TCS ECU sender")
#     p2 = Process(target=tcs_main, args=(Output_Port, )) # In TCS_process.py to start sender ports
#     p2.start()

def Acc_Pedal_Call(Output_Port):
    acc_pedal_main(Output_Port)

def TCS_Switch_Call(Output_Port1, Output_Port2):
    tcs_switch_main(Output_Port1, Output_Port2)

def Call_Server_Functions_Of_UseCases(threadName):
    global Chosen_Use_Cases

    print("Starting Server thread")

    if Create_Flag == 1:
        for receiver in Receiver_List:  # Components in the "Output" column in GUI
            if receiver == 'Hydraulic Modulator':
                p1 = Process(target=Hydraulic_Modulator_Call)
                p1.start()

            if receiver == 'Gateway':
                p2 = Process(target=Gateway_function)
                p2.start()

    elif Create_Flag == 0:

        p3 = Process(target=Gateway_function)
        print("Starting Gateway function")
        p3.start()

        if "Anti Lock Braking System" in Chosen_Use_Cases:
            print("Running ABS Server")
            # subprocess.run("python3 ABS_servers.py", shell=True)
            p1 = Process(target=abs_recv)
            print("Starting ABS ECU server")
            p1.start()
            # p1 = Process(target=ABS_ECU_Run_Threads, args=(5010, 5003, ))
            # print("Starting ABS ECU threads")
            # p1.start()

            p2 = Process(target=Hydraulic_Modulator_Call)
            print("Starting Hydraulic Modulator")
            p2.start()

        if "Traction Control System" in Chosen_Use_Cases:
            print("Running TCS Servers")
            # p4 = Process(target=TCS_ECU_Call, args=(5003, ))        # To connect to CAN bus
            # print("Starting TCS ECU")
            # p4.start()
            print("Starting TCS ECU receiver")
            p4 = Process(target=tcs_recv)       # In TCS_recv.py
            p4.start()

            p5 = Process(target=Instrument_Cluster_Call)
            print("Starting Instrument Cluster")
            p5.start()

            p6 = Process(target=ECM_Call)
            print("Starting ECM")
            p6.start()


        # elif "Right Turn and Return to Centre" in Chosen_Use_Cases:
        #     print("Running RT+RTC Servers")
        #     subprocess.run("python3 RT_servers.py", shell=True)



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
                p2 = Process(target=ADAS_Call, args=(6, temp_port2, ))
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

    elif Create_Flag == 0:
        if "Anti Lock Braking System" in Chosen_Use_Cases:
            print("Running ABS Clients")
            # subprocess.run("python3 ABS_Clients.py", shell=True)
            # print("----------------------------------------In ABS_Clients.py------------------------------------------")
            p1 = Process(target=WheelSpeed_Call, args=(5005, ))
            print("Starting Wheel speed sensor")
            p1.start()

            p2 = Process(target=ADAS_Call, args=(6, 5003, ))
            print("Starting ADAS")
            p2.start()

            p3 = Process(target=Brake_pedal_Call, args=(5005, ))
            print("Starting Brake Pedal sensor")
            p3.start()

            p4 = Process(target=ABS_ECU_Main, args=(5010, 5003, ))
            print("Starting ABS ECU client")
            p4.start()

        if "Traction Control System" in Chosen_Use_Cases:
            print("Running TCS Clients")
            p4 = Process(target=WheelSpeed_Call, args=(6001, ))
            print("Starting Wheel speed sensor")
            p4.start()

            p5 = Process(target=ADAS_Call, args=(4, 5003, ))
            print("Starting ADAS")
            p5.start()

            p6 = Process(target=Acc_Pedal_Call, args=(6001, ))
            print("Starting Brake Pedal sensor")
            p6.start()

            p7 = Process(target=TCS_Switch_Call, args=(6001, 6002, ))
            print("Starting TCS Switch")
            p7.start()

            print("Starting TCS ECU sender")
            p8 = Process(target=tcs_main, args=(5003, )) # In TCS_process.py to start sender ports
            p8.start()
        #
        # if "Right Turn and Return to Centre" in Chosen_Use_Cases:
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
            subprocess.run("python3 CAN_Bus_No_Optimization.py", shell=True)

        else:
            print("You have not answered for all questions")

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

        # print(f"Selected use cases visible in Run_Use_case function are {Selected_Use_Cases}")

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

class Select_UseCases(Frame):
    global root
    global choices
    global Chosen_Use_Cases

    def __init__(self, parent, **kw):
        Frame.__init__(self, parent)
        super().__init__(**kw)
        menubutton = Menubutton(self, text="Choose Use cases") #indicatoron=True, borderwidth=1, relief="raised"
        menu = Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        menubutton.grid(row=15, column =0)

        #choices = {}
        for choice in ("Anti Lock Braking System", "Traction Control System", "Right Turn and Return to Centre", "Cruise Control", "Tire Pressure Monitoring System"):
            choices[choice] = IntVar(value=0)
            menu.add_checkbutton(label=choice, variable=choices[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.printValues)


    def printValues(self):
        for name, var in choices.items():
            print("%s: %s" % (name, var.get()))
            if var.get() == 1:
                Chosen_Use_Cases.append(name)
        print(f"Chosen_Use_Cases are {Chosen_Use_Cases}")


################## Create New use case functions#####################################################################
def Add_Labels(root, top_frame):   # Add columns
    global Current_Row

    frame1 = Frame(top_frame)
    frame1.grid(column=0, row=0, sticky='new')

    for i in range(1,4):
        frame1.grid_columnconfigure(i, weight=3, uniform='columns')

    for Num_Of_Fields in range(1,4):  # Three = Component, its inputs and outputs
        print(f"Current row is {Current_Row} and Column is {Num_Of_Fields}")
        e = Entry(root)
        e.grid(row=Current_Row, column=Num_Of_Fields, sticky=W)
        # e.grid_columnconfigure(Num_Of_Fields, weight = 2)
        if Num_Of_Fields == 1:  # Components column
            e.insert(0, 'Inputs')
            print(f"Added Label")

        elif Num_Of_Fields == 2:    # Inputs Column
            e.insert(0, 'Components')

        elif Num_Of_Fields ==3:     # Outputs Column
            e.insert(0, 'Outputs')



def Add_Component(root, Components_List):
    global Current_Row

    for Num_Column in range(1,4):  # Three = Component, its inputs and outputs

        print(f"Num_Of_Fields is {Num_Column}")
        # Naming each column
        if Num_Column == 1:  # Components column
            # e.insert(0, 'Component')
            b1 = Combobox(root, state = 'readonly', values = Components_List)
            b1.bind("<<ComboboxSelected>>", partial(Print_and_Save, Num_Column))
            b1.current(0)
            b1.grid(row=Current_Row+1, column=Num_Column)
            print(f"Current_Row with Column number 0 is {Current_Row}")

        elif Num_Column == 2:    # Inputs Column
            # e.insert(0, 'Inputs')
            b2 = Combobox(root, state = 'readonly', values = Components_List)
            b2.bind("<<ComboboxSelected>>", partial(Print_and_Save, Num_Column))
            b2.current(0)
            b2.grid(row=Current_Row+1, column=Num_Column)

            print(f"Current_Row with Column number 1 is {Current_Row}")

        elif Num_Column ==3:     # Outputs Column
            # e.insert(0, 'Outputs')
            b3 = Combobox(root, state = 'readonly', values = Components_List)
            b3.bind("<<ComboboxSelected>>", partial(Print_and_Save, Num_Column))
            b3.current(0)
            b3.grid(row=Current_Row+1, column=Num_Column)
            print(f"Current_Row with Column number 2 is {Current_Row}")


def Print_and_Save(cb_number, event):

    global Current_Row
    global Selected_Components_Array
    global local_index

    # if Current_Row == 1:
    #     local_index = 0

    print(f"Current_Row in Print and Save function is {Current_Row}")
    print("Current Column number is ", cb_number, "SelectedValue",  event.widget.get())
    print(f"local_index is {local_index} and Selected_Components_Array[local_index] is {Selected_Components_Array[local_index]}")

    Selected_Components_Array[local_index].append(event.widget.get())    # Keep on adding each row in 1 sub-array to get final multi dimensional array of selected components
    print("Selected_Components_Array is", Selected_Components_Array)

    if cb_number == 2:        # If there is no event and user has selected all 3 drop down values for first row
        print("As this is the last column ----------")  # As Component and its input and output are selected,
        Current_Row += 1
        local_index += 1     # Make it 0 again to start filling data in Selected_Components_Array in next loop
        print("Current Row is now changed in print and save loop to ", Current_Row)

def Connect_Components():
    global Connection_Port_Dictionary
    global Receiver_List
    global Default_Component_Port_Dictionary

    for Row in Selected_Components_Array:
        Row_Index_Flag = 0  # To know that the item in below loop is "Input"
        print("Row_Index_Flag is now reset to ", Row_Index_Flag)
        Previous_element = 0

        for item in Row:
            Value_List = []

            if Row_Index_Flag == 0:     # Element in zeroth index .i.e. Input
                # print("Flag is", Row_Index_Flag)
                Previous_element = item
            elif Row_Index_Flag == 1:       # Element in 1th index .i.e. Component
                # print("Flag is", Row_Index_Flag)
                temp_port = Default_Component_Port_Dictionary[item]
                print("Row_Index_Flag is ", Row_Index_Flag)
                Value_List.append(temp_port)

                if Previous_element in Connection_Port_Dictionary.keys():
                    if Connection_Port_Dictionary[Previous_element] != temp_port:   # If not the same value again
                        print("Temp port is ", temp_port)
                        print("Connection_Port_Dictionary[Previous_element] is ", Connection_Port_Dictionary[Previous_element])
                        print("Appending value as the same key exists")
                        Connection_Port_Dictionary[Previous_element].append(temp_port)
                else:
                    Connection_Port_Dictionary[Previous_element] = Value_List
                print("Connection ports array is ", Connection_Port_Dictionary)
                Previous_element = item

            elif Row_Index_Flag == 2:                           # Element in 2nd index .i.e. Output
                # print("Flag is", Row_Index_Flag)
                temp_port = Default_Component_Port_Dictionary[item]
                print("Row_Index_Flag is ", Row_Index_Flag)
                Value_List.append(temp_port)

                if item not in Receiver_List:
                    Receiver_List.append(item)  # Use the final list of only receivers in Call_Server_Functions_Of_UseCases() function

                if Previous_element in Connection_Port_Dictionary.keys():
                    if Connection_Port_Dictionary[Previous_element] != temp_port:   # If not the same value again
                        print("Temp port is ", temp_port)
                        print("Connection_Port_Dictionary[Previous_element] is ", Connection_Port_Dictionary[Previous_element])
                        print("Appending value as the same key exists")
                        Connection_Port_Dictionary[Previous_element].append(temp_port)
                else:
                    Connection_Port_Dictionary[Previous_element] = Value_List
                print("Connection ports array is ", Connection_Port_Dictionary)
                Previous_element = item
            else:
                print("Row_Index_Flag in else loop is", Row_Index_Flag)
                print("Value out of Index")

            Row_Index_Flag+=1


    # To eliminate repeated values of each key
    for k in Connection_Port_Dictionary.keys():
        Connection_Port_Dictionary[k] = set(Connection_Port_Dictionary[k])

    Receiver_List = set(Receiver_List)  # To eliminate repeated names
    print(f"Receiver_List is {Receiver_List}")



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

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    ################### Create Use Case function ####################################################
    top_frame = Frame(root, width =500, height=500) #
    top_frame.grid(row=0, column=0, sticky='new')
    # root.grid_rowconfigure(0, weight=1)
    top_frame.grid_columnconfigure(0, weight=3)


#----------------------------------------
    # frame1 = Frame(top_frame)
    # frame1.grid(column=0, row=0, sticky='new')
    # for i in range(1,4):
    #     frame1.grid_columnconfigure(i, weight=3, uniform='columns')
    #
    # for i in range(1, 4):
    #     header = Label(frame1, text=f'Header {i}')
    #
    #     header['relief'] = 'solid'
    #     header['borderwidth'] = 1
    #     # header['highlightthickness'] = 1
    #     # header['highlightbackground'] = 'grey65'
    #     header.grid(column=i, row=0, sticky='ew')
#-------------------------------------------
    Row = 10
    Column = 3
    Current_Component_Selections_Array = []
    Selected_Components_Array = [[] for i in range(10)]
    Default_Component_Port_Dictionary = {'ABS ECU': 5005, 'Gateway': 7400, 'CAN Bus': 5003, 'Hydraulic Modulator': 5010, 'Assist_Motor':5025, 'ECM':5065, 'Instrument Cluster':6002, 'Load Motor': 5044}
    ####################################################################################################

    # # Add text
    Text_Baud1 = Label(root, text = "Select components below to create a new use case ")
    Text_Baud1.grid(row=0, column=1,columnspan=3)

    #----------------------------------Create New use case field------------------------------------------
    Components_List = ['Wheel Speed Sensor', 'Brake Pedal Sensor', 'Vehicle Speed Sensor', 'Angle Sensor', 'Torque Sensor', 'ABS ECU', 'ADAS ECU', 'EPS ECU',
                       'Gateway', 'CAN Bus', 'Assist Motor', 'Load Motor', 'Rack and Pinion', 'Hydraulic Modulator']


    Add_Labels(root, top_frame)
    Add_Component(root, Components_List)

    B1 = Button(root, text='Add Component', command=partial(Add_Component, root, Components_List)).grid(row=10,column=1,columnspan=3)
    B2 = Button(root, text='Create New Use Case', command=Connect_Components).grid(row=11,column=1,columnspan=3)
    B3 = Button(root, text='Exit', command=root.destroy).grid(row=12,column=1,columnspan=3)


    #
    ################### Run Use Case function####################################################
    #----------------------------------------------------------------------------
    ##### User will select the use cases that needs to be run

    # Add text
    Empty1 = Label(root, text = " ").grid(row=13, column =1,columnspan=3)
    Empty2 = Label(root, text = " ").grid(row=14, column =1,columnspan=3)
    Empty3 = Label(root, text = " ").grid(row=15, column =1,columnspan=3)
    #----------------------------------------------------------------------------



    ##### User will select the use cases that needs to be run

    # Add text
    Text_Baud1 = Label(root, text = "Please select all the use cases that you want to execute: ")
    Text_Baud1.grid(row=17, column =1,columnspan=3)

    Select_UseCases(root).grid(row=18, column =1,columnspan=3)
    #----------------------------------------------------------------------------
    ##### Ask user if they want to apply optimization technique

    # Add text
    Text_Baud2 = Label(root, text = "Apply optimization technique?")
    Text_Baud2.grid(row=19, column =1,columnspan=3)

    Temp_apply = StringVar(value="Select")
    options2 = ('Yes',
                'No')

    Selected_Apply_option = Combobox(root, width = 50, state='readonly', value=options2)

    Selected_Apply_option.current()
    Selected_Apply_option.bind("<<Combobox2selected>>", Selected_Apply_option)
    Selected_Apply_option.grid(row=20, column =1,columnspan=3)

    #----------------------------------------------------------------------------
    ##### Ask user which optimization technique should be applied

    Text_Baud3 = Label(root, text = "Which optimization technique?")
    Text_Baud3.grid(row=21, column =1,columnspan=3)

    # Select Attacker Sensor type from drop down
    options3 = ('Simulated Annealing - For Congestion',
                'Simulated Annealing - For Latency',
                'None')

    # Combobox(root, width = 50, value=options3, textvariable = Selected_Opt_Technique).pack()
    Selected_Opt_Technique = Combobox(root, width = 50, value=options3)

    Selected_Opt_Technique.current()
    Selected_Opt_Technique.bind("<<Combobox2selected>>", Selected_Opt_Technique)
    Selected_Opt_Technique.grid(row=22, column =1,columnspan=3)
    # Selected_Opt_Technique = Field3.get()
    # print(f"Selected_Opt_Technique is {Selected_Opt_Technique}")
    #----------------------------------------------------------------------------
    # Run button
    # print("Gonna run Run_Use_case function")
    B1 = Button(root, text="Run and Get Results", width = 20, command=Run_Use_cases)        # Need to call Trigger_Attack() function to start Attacker sensor
    B1.grid(row=23, column =1,columnspan=3)

    # Stop button
    B2 = Button(root, text="Stop", width = 20, command=Stop_function)
    B2.grid(row=24, column =1,columnspan=3)

    # Create button
    # print("Gonna run Run_Use_case function")
    B3 = Button(root, text="Create", width = 20, command=Create_Main_Function)        # This should set Create_Flag to 1
    B3.grid(row=25, column =1,columnspan=3)

    mainloop()

if __name__ == '__main__':
    main()







