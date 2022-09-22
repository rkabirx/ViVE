import socket
from tkinter import *
from tkinter.ttk import *
from time import strftime, time
from tkinter.messagebox import *
import _thread

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
    No_Attack_Complete_Flag = 1
    print(f"Stop flag is turned to {Stop_Flag} and No_Attack_Complete_Flag is {No_Attack_Complete_Flag}")

def Call_Server_Functions_Of_UseCases(threadName):
    global choices

    if "Anti Lock Braking System" in choices:
        import ABS_Call
        ABS_Call

        print("Running ABS")


    elif "Traction Control System" in choices:
        import Gateway

        print("Running TCS Servers")
        Gateway_Main()


    elif "Right Turn and Return to Centre" in choices:
        import Gateway

        print("Running RT+RTC Servers")
        Gateway_Main()


    elif "Cruise Control" in choices:
        import Gateway
        print("Running Cruise Control Servers")
        Gateway_Main()

    elif "Tire Pressure Monitoring System" in choices:
        import Gateway
        print("Running TPMS Servers")
        Gateway_Main()

def Call_Client_Functions_Of_UseCases(threadName):
    if "Anti Lock Braking System" in choices:
        import ABS_clients

        print("Running ABS Clients")
        ABS_Clients_Main()

    elif "Traction Control System" in choices:
        print("Running TCS Clients")

    elif "Right Turn and Return to Centre" in choices:
        print("Running RT+RTC Clients")

    elif "Cruise Control" in choices:
        print("Running Cruise Control Clients")

    elif "Tire Pressure Monitoring System" in choices:
        print("Running TPMS Clients")


def Run_Use_cases():
    try:
        # global Attack_Flag
        global Stop_Flag
        # global No_Attack_Complete_Flag
        global Selected_Use_Cases
        global Selected_Apply_option
        global Selected_Opt_Technique
        global root
        global choices
        global Run_Flag

        Run_Flag = 1
        print("In Run_Use_Case function")
        print(f"Run Flag is {Run_Flag}")

        if Run_Flag == 1:
            import CANBus_Congestion
            import CANBus_Latency
            # import ABS_servers
            # import RT_servers
            # import TCS_servers
            import TCS_clients
            import ABS_clients
            import RT_clients
            import Gateway

        # Start CAN Bus and optimization code first
        if Selected_Apply_option == 'Yes':
            if Selected_Opt_Technique == 'Simulated Annealing - For Congestion':
                print("Running congestion")
                CANBus_Congestion_Main()

            elif Selected_Opt_Technique == 'Simulated Annealing - For Latency':
                print("Running Latency")
                CANBus_Latency_Main()

            else:   # None case
                showerror("error", "You need to select a technique")

        else:       # No optimization case
            print("Run use cases without optimization function")

        # Run use cases as per selection  # Create two threads as follows
        try:
            _thread.start_new_thread( Call_Server_Functions_Of_UseCases, ("Server Thread", ) )
            time.sleep(2)
            _thread.start_new_thread( Call_Client_Functions_Of_UseCases, ("Client Thread", ) )
        except:
            print("Error: unable to start thread")

        if Stop_Flag == 1:
            root.after(2000, lambda: showerror("error", "Stopping current functionality"))
            Stop_Flag = 0

    except KeyboardInterrupt:
        exit()

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
    # print("Here in main")

    # creating tkinter window
    root = Tk()
    root.title('Virtual Platform')
    #root.configure(background = "black")
    # Creating Menubar
    menubar = Menu(root)

    # Adding Attack Menu and commands
    attack = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Run Use Cases', menu=attack)
    #attack.add_command(label='Sensor Attack', command=Sensor_Attack)

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

    # Select Attacker Sensor type from drop down
    #Temp_Variable = StringVar()
    options2 = ('Yes',
                'No')
    #SensorChosen.grid(column= 1, row= 3)
    Field2 = Combobox(root, width = 50, value=options2)
    Field2.current()
    Field2.bind("<<Combobox2selected>>", Field2)
    Field2.pack()

    # #Error if different status
    Selected_Apply_option = Field2.get()
    print(f"Selected Apply option is {Selected_Apply_option}")
    #----------------------------------------------------------------------------
    ##### Ask user which optimization technique should be applied

    Text_Baud = Label(root, text = "Which optimization technique?")
    Text_Baud.pack()

    # Select Attacker Sensor type from drop down
    options3 = ('Simulated Annealing - For Congestion',
                'Simulated Annealing - For Latency',
                'None')

    Field3 = Combobox(root, width = 50, value=options3)
    Field3.current()
    Field3.bind("<<Combobox2selected>>", Field3)
    Field3.pack()
    Selected_Opt_Technique = Field3.get()
    #----------------------------------------------------------------------------
    # Run button
    # print("Gonna run Run_Use_case function")
    B1 = Button(root, text="Run and Get Results", width = 20, command=Run_Use_cases)        # Need to call Trigger_Attack() function to start Attacker sensor
    B1.pack()

    # Stop button
    B3 = Button(root, text="Stop", width = 20, command=Stop_function)
    B3.pack()

    # display Menu
    root.config(menu=menubar)
    mainloop()

if __name__ == '__main__':
    main()


