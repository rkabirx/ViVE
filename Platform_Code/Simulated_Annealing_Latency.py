import math
import random
# import visualize_tsp

import copy

class SimAnneal(object):
    def __init__(self, Packets, Sorted_Dict, Maximum_Congestion_Allowed, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.Packets = Packets
        # self.temp_Packets = self.Packets
        self.T = 20         # Value could be math.sqrt(self.Length_Of_Packets) if T == -1 else T -> in other codes
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        self.alpha = 0.795 if alpha == -1 else alpha
        self.stopping_temperature = 8       # This value is  = 1e-8 if stopping_T == -1 else stopping_T in other codes
        self.stopping_iter = 10         # Value could be 100000 if stopping_iter == -1 else stopping_iter -> In other codes
        self.iteration = 1
        # self.Reprioritized_SequenceOfPackets = []
        self.Sorted_Dict = Sorted_Dict
        self.highest_constraint = 0
        self.n = len(self.Packets)        # It represents the number of packets that there can be in a cycle - Lets initiate it with highest congestion .i.e. all packets in 1 cycle
        # self.highest_constraint = 0
        self.Default_Cycles_array = []
        self.Cycles_array =[]   # Created multi-dimensional array in which each row represents one cycle of the optimizer
        n = 1000  # Column represent the number of threads or number of clients
        m = 1500 # Row represent the length of the stored data of each client
        self.Final_Array_Of_Valid_Sequences = [[] * m] * n
        # self.Final_Array_Of_Valid_Sequences = []
        self.Final_Array_Index = 0     # Navigate through Sorted values list to decide the range of cycles in which packet is allowed to transmit
        self.Get_Sequence_Flag = 0
        self.least_peak_delay = 0
        self.least_average_delay = 0
        self.best_sequence = []
        self.second_least_peak_delay = 0
        self.second_least_average_delay = 0
        self.second_best_sequence = []
        self.Maximum_Congestion_Allowed = Maximum_Congestion_Allowed

    ###### Function to put allocate each packet in default cycle to get default sequence -> Make first choice of Simulated Annealing
    def Find_Sequence(self,Temp_Packets):
        Temp_Sequence = []
        # Calculating sequence
        index = 0
        Num_of_cycles_required = int((len(Temp_Packets)+1)/self.Maximum_Congestion_Allowed)
        print(f"Num_of_cycles_required is {Num_of_cycles_required}")
        print(f"Current Temp_Packets is {Temp_Packets}")
        for r in range(Num_of_cycles_required):
            row = []
            for c in range(self.Maximum_Congestion_Allowed):
                if index < len(Temp_Packets):
                    row.append(Temp_Packets[index])
                    index += 1
            Temp_Sequence.append(row)
        print(f"Temp Sequence is {Temp_Sequence}")
        self.Final_Array_Of_Valid_Sequences[self.Final_Array_Index] = Temp_Sequence
        self.Final_Array_Index = self.Final_Array_Index+1

    def swap(self,a,b):
        # temp_var = 0
        temp_var = a
        a = b
        b = temp_var
        return a,b

    def Get_Array_of_Sequences(self,Packets):

        ## To get permutation of all elements in packets
        temp_var = 0
        Temp_Sequence = []
        Temp_Packets = copy.deepcopy(Packets)

        for temp_index in range(0, len(Packets)):

            self.T = self.T-1 # Reducing T      # Could be written as self.T *= self.alpha
            self.iteration += 1 # Increasing Iteration
            print(f"\nCurrent Sequence with Reduced Temperature = {self.T} and Iteration number {self.iteration}")

            print(f"For element {Temp_Packets[temp_index]}")

            if temp_index >= 1:
                ## To get variation of sequences in a single array
                a,b = self.swap(Temp_Packets[temp_index], Temp_Packets[temp_index-1])
                print(f"a,b are {a} and {b}")
                Temp_Packets[temp_index] = a
                Temp_Packets[temp_index-1] = b
                print(f"Temp packet is {Temp_Packets}")


            self.Find_Sequence(Temp_Packets)

        print(f"self.Final_Array_Of_Valid_Sequences is {self.Final_Array_Of_Valid_Sequences} ")
        self.Get_Sequence_Flag = 1



    def p_accept(self, average_congestion):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(average_congestion - self.least_average_delay) / self.T)

        # print(f"In Default function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")
        # print(f"In Default function-> Updated Final_array_index is {self.Final_Array_Index}")


    def Calculate_Delay(self, Sequence):

        Last_Packet_Number = self.Packets[-1]
        Sequence_with_Congestion = copy.deepcopy(Sequence)
        print(f"Sequence_with_Congestion is {Sequence_with_Congestion} with length {len(Sequence_with_Congestion)}")

        for cycle in range(1, len(Sequence_with_Congestion)):
            # if cycle == 1:
            # print(f"Sequence_with_Congestion[cycle] is {Sequence_with_Congestion[cycle]}")
            for temp_pack in range(0, len(Sequence_with_Congestion[cycle])):
                print(f"temp_pack is {temp_pack}")
                Congestion = self.Sorted_Dict[Sequence_with_Congestion[cycle-1][temp_pack]]
                print(f"Congestion is {Congestion}")

                # To get the new estimated packets in the current cycle as per congestion caused by previous cycle
                for new_pack in range(0, Congestion):
                    Last_Packet_Number += 1
                    print(f"Last_Packet_Number added in array is {Last_Packet_Number}")
                    Sequence_with_Congestion[cycle].append(Last_Packet_Number)
            print(f"Updated Sequence_with_Congestion for 1 cycle is {Sequence_with_Congestion}")
        print(f"Updated Sequence_with_Congestion for all cycle is {Sequence_with_Congestion}")

        Initial_Cycle_Dict = {}       # Global value

        # Length_of_Sequence_with_Congestion = (Sequence_with_Congestion[-1][-1]) +1
        # # print(f"Length_of_Sequence_with_Congestion is {Length_of_Sequence_with_Congestion}")

        Distributed_Sequence_with_Congestion = []       # Local array
        Integrated_Sequence_with_Congestion = []        # Local array

        for cycle in range(0, len(Sequence_with_Congestion)):
            # print(f"For cycle {cycle}")
            for temp_pack_index in range(0, len(Sequence_with_Congestion[cycle])):
                ## To create a dictionary of packet: Packet's initially estimated cycle so that we can use it later to compare with its actual cycle to calculate delay
                Initial_Cycle_Dict[Sequence_with_Congestion[cycle][temp_pack_index]] = cycle

                ## Creating an integrated array of all packets in Sequence_with_Congestion to distribute it later in small sub-arrays
                Integrated_Sequence_with_Congestion.append(Sequence_with_Congestion[cycle][temp_pack_index])
        print(f"\nInitial_Cycle_Dict is {Initial_Cycle_Dict}")
        # print(f"Integrated_Sequence_with_Congestion is {Integrated_Sequence_with_Congestion}")

        temp_index = 0
        Num_of_cycles_required = int((len(Integrated_Sequence_with_Congestion)+1)/self.Maximum_Congestion_Allowed)
        # print(f"Num_of_cycles_required is {Num_of_cycles_required}")
        # print(f"Initial temp index is {temp_index}")
        # print(f"len(Integrated_Sequence_with_Congestion) is {len(Integrated_Sequence_with_Congestion)}")

        for r in range(Num_of_cycles_required):
            # if temp_index < len(Integrated_Sequence_with_Congestion):
            # print(f"In If loop because temp_index {temp_index} is smaller than len(Integrated_Sequence_with_Congestion) {len(Integrated_Sequence_with_Congestion)}")
            row = []
            # print(f"r is {r}")
            for c in range(self.Maximum_Congestion_Allowed):
                if temp_index < len(Integrated_Sequence_with_Congestion):
                    # print(f"c is {c} and Integrated_Sequence_with_Congestion is {Integrated_Sequence_with_Congestion}")
                    # print(f"row is {row}")
                    # print(f"temp index is {temp_index}")
                    row.append(Integrated_Sequence_with_Congestion[temp_index])
                    temp_index += 1
            Distributed_Sequence_with_Congestion.append(row)
            # print(f"Distributed_Sequence_with_Congestion is {Distributed_Sequence_with_Congestion}")


        Delayed_Cycle_Dict = {}       # Global value

        for cycle in range(0, len(Distributed_Sequence_with_Congestion)):
            # print(f"For cycle {cycle}")
            for temp_pack_index in range(0, len(Distributed_Sequence_with_Congestion[cycle])):
                # print(f"Current packet is {Sequence_with_Congestion[cycle][temp_pack_index]}")
                ## To create a dictionary of packet: Packet's delayed cycle so that we can use it later to compare with its estimated cycle to calculate delay
                Delayed_Cycle_Dict[Distributed_Sequence_with_Congestion[cycle][temp_pack_index]] = cycle
        print(f"Delayed_Cycle_Dict is {Delayed_Cycle_Dict}")

        Peak_Delay = 0
        Average_Delay = 0
        Sum_of_Delay = 0
        for temp_pack in Integrated_Sequence_with_Congestion:
            Delay = Delayed_Cycle_Dict[temp_pack] - Initial_Cycle_Dict[temp_pack]
            ## Get Peak Delay
            if Delay > Peak_Delay:
                Peak_Delay = Delay
            ## Get Average Delay
            Sum_of_Delay += Delay

        Average_Delay = Sum_of_Delay/len(Integrated_Sequence_with_Congestion)

        ## Delay without optimization -> Without optimizer, maximum delay will be when packet at index is sent in the last cycle
        Peak_Delay_without_Optimizer = len(Distributed_Sequence_with_Congestion) - 2

        print(f"Average Delay for this sequence is {Average_Delay}")
        print(f"Peak Delay for this sequence is {Peak_Delay}\n")
        return Peak_Delay, Average_Delay, Peak_Delay_without_Optimizer


    def Simulated_Anneal(self):

            Sorted_Values = []
            for i in self.Sorted_Dict.keys():
                if self.Sorted_Dict[i] not in Sorted_Values:
                    Sorted_Values.append(self.Sorted_Dict[i])
            Sorted_Values.sort()
            # print(f"Sorted values list of congestion is : {Sorted_Values}")
            self.highest_constraint = Sorted_Values[-1]
            lowest_constraint = Sorted_Values[0]

            # Format of multi dim array command -> [[]*Columns for i in range(Rows OR Sub-Arrays)]
            # self.Default_Cycles_array =[]
            self.Cycles_array =[[]*self.n for i in range(self.highest_constraint)]   # Created multi-dimensional array in which each row represents one cycle of the optimizer
            self.Final_Array_Of_Valid_Sequences = [[]*500 for i in range(500)]

            #Call the default function first->  Get 1 valid sequence first

            # self.Find_Default_Sequence(self.Packets)
            # Loop to get all valid sequences
            print("\nStarting Simulated Annealing.")
            while self.T >= self.stopping_temperature and self.iteration <= self.stopping_iter and self.Get_Sequence_Flag != 1:
                print(f"T = {self.T} and iteration number {self.iteration}")
                self.Get_Array_of_Sequences(self.Packets)

            #Call function to calculate Congestion in the sequence
            for sequence in self.Final_Array_Of_Valid_Sequences:
                if sequence:
                    print(f"Current sequence in consideration is {sequence}")
                    temp_peak_delay, temp_average_delay, Peak_Delay_without_Optimizer = self.Calculate_Delay(sequence)

                    #### Compare current congestion with congestion of saved sequences
                    if self.second_least_peak_delay == 0 and self.least_peak_delay == 0:  # Initialize all values for the first loop as no value would be smaller than 0.
                        self.second_best_sequence = sequence
                        self.second_least_peak_delay = temp_peak_delay
                        self.second_least_average_delay = temp_average_delay
                        self.best_sequence = sequence
                        self.least_peak_delay = temp_peak_delay
                        self.least_average_delay = temp_average_delay

                    if temp_peak_delay < self.second_least_peak_delay or temp_average_delay < self.second_least_average_delay:
                        self.second_best_sequence = sequence
                        self.second_least_peak_delay = temp_peak_delay
                        self.second_least_average_delay = temp_average_delay
                        if temp_peak_delay < self.least_peak_delay or temp_average_delay < self.least_average_delay:
                            # print("Inside Second if loop")
                            # print(f"Initial least_peak_congestion is {self.least_peak_congestion}")
                            # print(f"Initial least_average_congestion is {self.least_average_congestion}")
                            self.best_sequence = sequence
                            self.least_peak_delay = temp_peak_delay
                            self.least_average_delay = temp_average_delay
                    else:
                        if random.random() < self.p_accept(temp_peak_delay):   # removed temp_average_congestion
                            # print("Inside Else loop")
                            self.second_best_sequence = sequence
                            self.second_least_peak_delay = temp_peak_delay
                            self.second_least_average_delay = temp_average_delay
                            # print(f"Initial second_least_peak_congestion is {self.second_least_peak_congestion}")
                            # print(f"Initial second_least_average_congestion is {self.second_least_average_congestion}")
            print("\n")
            print(f"Best Sequence obtained: {self.best_sequence}")
            print(f"Least Peak Delay: {self.least_peak_delay}")
            print(f"Least Average Delay: {self.least_average_delay}")
            print(f"Delay without Optimizer is {Peak_Delay_without_Optimizer}")

            return self.best_sequence, self.least_peak_delay, self.least_average_delay, Peak_Delay_without_Optimizer









