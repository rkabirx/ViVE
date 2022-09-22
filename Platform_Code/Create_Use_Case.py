from tkinter import *
from functools import partial
from tkinter.ttk import *


Current_Row=1
Connection_Port_Dictionary = {}
Create_Flag = 0
Receiver_List = []

class Create_GUI:
    global Current_Row
    global Connection_Port_Dictionary
    global Receiver_List

    def __init__(self, Components_List):
        self.top = Tk()
        self.top.title('Create New Use Case')
        self.top_frame = Frame(self.top, width =400, height=400)
        self.button_dic = {}
        self.combos_dic = {}
        self.var = StringVar()
        self.top_frame.grid(row=0, column=4)
        self.Components_List = Components_List
        self.Add_Labels()
        self.Add_Component()
        self.Row = 10
        self.Column = 3
        self.Current_Component_Selections_Array = []
        self.Selected_Components_Array = [[] for i in range(10)]
        self.Default_Component_Port_Dictionary = {'ABS ECU': 5005, 'Gateway': 7400, 'CAN Bus': 5003, 'Hydraulic Modulator': 5010, 'Assist_Motor':5025, 'ECM':5065, 'Instrument Cluster':6002, 'Load Motor': 5044}
        # Receiver sides only ( Either Component list or output list)


        B1 = Button(self.top, text='Add Component', command=self.Add_Component).grid(row=4,column=3,columnspan=10)
        B2 = Button(self.top, text='Create New Use Case', command=self.Connect_Components).grid(row=10,column=0,columnspan=10)
        B3 = Button(self.top, text='Exit', command=self.top.destroy).grid(row=11,column=0,columnspan=10)
        self.top.mainloop()

    def Add_Labels(self):   # Add columns
        global Current_Row

        for Num_Of_Fields in range(3):  # Three = Component, its inputs and outputs
            e = Entry(self.top_frame)
            e.grid(row=Current_Row, column=Num_Of_Fields)
            if Num_Of_Fields == 0:  # Components column
                e.insert(0, 'Inputs')
                print(f"Added Label")

            elif Num_Of_Fields == 1:    # Inputs Column
                e.insert(0, 'Components')

            elif Num_Of_Fields ==2:     # Outputs Column
                e.insert(0, 'Outputs')

    def Add_Component(self):
        global Current_Row

        for Num_Column in range(3):  # Three = Component, its inputs and outputs

            print(f"Num_Of_Fields is {Num_Column}")
            # Naming each column
            if Num_Column == 0:  # Components column
                # e.insert(0, 'Component')
                b1 = Combobox(self.top_frame, state = 'readonly', values = self.Components_List)
                b1.bind("<<ComboboxSelected>>", partial(self.Print_and_Save, Num_Column))
                b1.current(0)
                b1.grid(row=Current_Row+1, column=Num_Column)
                print(f"Current_Row with Column number 0 is {Current_Row}")

            elif Num_Column == 1:    # Inputs Column
                # e.insert(0, 'Inputs')
                b2 = Combobox(self.top_frame, state = 'readonly', values = self.Components_List)
                b2.bind("<<ComboboxSelected>>", partial(self.Print_and_Save, Num_Column))
                b2.current(0)
                b2.grid(row=Current_Row+1, column=Num_Column)

                print(f"Current_Row with Column number 1 is {Current_Row}")

            elif Num_Column ==2:     # Outputs Column
                # e.insert(0, 'Outputs')
                b3 = Combobox(self.top_frame, state = 'readonly', values = self.Components_List)
                b3.bind("<<ComboboxSelected>>", partial(self.Print_and_Save, Num_Column))
                b3.current(0)
                b3.grid(row=Current_Row+1, column=Num_Column)
                print(f"Current_Row with Column number 2 is {Current_Row}")


    def Print_and_Save(self, cb_number, event):

        global Current_Row

        print(f"Current_Row in Print and Save function is {Current_Row}")
        print("Current Column number is ", cb_number, " SelectedValue",  event.widget.get())
        print(f"Current_Row-1 is {Current_Row-1} and self.Selected_Components_Array[Current_Row-1] is {self.Selected_Components_Array[Current_Row-1]}")
        self.Selected_Components_Array[Current_Row-1].append(event.widget.get())    # Keep on adding each row in 1 sub-array to get final multi dimensional array of selected components
        print("self.Selected_Components_Array is", self.Selected_Components_Array)

        if cb_number == 2:        # If there is no event and user has selected all 3 drop down values for first row
            print("As this is the last column ----------")  # As Component and its input and output are selected,
            Current_Row += 1
            print("Current Row is now changed in print and save loop to ", Current_Row)

    def Connect_Components(self):
        global Connection_Port_Dictionary
        global Receiver_List

        for Row in self.Selected_Components_Array:
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
                    temp_port = self.Default_Component_Port_Dictionary[item]
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
                    temp_port = self.Default_Component_Port_Dictionary[item]
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
                    print("Row_Index_Flag is", Row_Index_Flag)
                    print("Value out of Index")

                Row_Index_Flag+=1

        # To eliminate repeated values of each key
        for k in Connection_Port_Dictionary.keys():
            Connection_Port_Dictionary[k] = set(Connection_Port_Dictionary[k])

        Receiver_List = set(Receiver_List)  # To eliminate repeated names
        print(f"Receiver_List is {Receiver_List}")

## Till now, I have been able to make a dictionary of which component should try to connect to which port.
## Next step would be to sync this up with the Run_Use Case page and to update that code such that
# the port values are taken from this dictionary to pass on to the client ans server functions in arguments to run it.


def Create_Main_Function():
    global Create_Flag

    Components_List = ['Wheel Speed Sensor', 'Brake Pedal Sensor', 'Vehicle Speed Sensor', 'Angle Sensor', 'Torque Sensor', 'ABS ECU', 'ADAS ECU', 'EPS ECU',
                       'Gateway', 'CAN Bus', 'Assist Motor', 'Load Motor', 'Rack and Pinion', 'Hydraulic Modulator']
    CT=Create_GUI(Components_List)
    Create_Flag = 1


if __name__ == '__main__':
    Create_Main_Function()