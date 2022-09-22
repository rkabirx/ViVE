import math
import random
# import visualize_tsp
import matplotlib.pyplot as plt
import copy

class SimAnneal(object):
    def __init__(self, Packets, Sorted_Dict, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
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
        n = 30  # Column represent the number of threads or number of clients
        m = 100 # Row represent the length of the stored data of each client
        self.Final_Array_Of_Valid_Sequences = [[] * m] * n
        # self.Final_Array_Of_Valid_Sequences = []
        self.Final_Array_Index = 0     # Navigate through Sorted values list to decide the range of cycles in which packet is allowed to transmit
        self.With_BackTrack_Flag = 0
        self.Without_BackTrack_Flag = 0
        self.least_peak_congestion = 0
        self.least_average_congestion = 0
        self.best_sequence = []
        self.second_least_peak_congestion = 0
        self.second_least_average_congestion = 0
        self.second_best_sequence = []

    ###### Function to put allocate each packet in default cycle to get default sequence -> Make first choice of Simulated Annealing
    def Find_Default_Sequence(self,Packets):
        # Calculating default sequence
        # print(f"In Find_Default_Sequence function-> Packets is {Packets}")
        # print(f"In Find_Default_Sequence function-> Sorted_Dict.keys is {Sorted_Dict.keys()}")

        for pack in Packets:
            print(f"Current packet is {pack}")
            max_cycle = self.Sorted_Dict[pack]
            # print(f"Max cycle for this packet in default sequence is {max_cycle}")
            self.Default_Cycles_array[max_cycle-1].append(pack)
            # print(f"Default Cycles list is {self.Default_Cycles_array}")
        # Put the default sequence in the first row of final array to track it
        self.Final_Array_Of_Valid_Sequences[self.Final_Array_Index] = self.Default_Cycles_array
        self.Final_Array_Index = self.Final_Array_Index+1
        # print(f"In Default function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")
        # print(f"In Default function-> Updated Final_array_index is {self.Final_Array_Index}")


    def With_BackTrack(self,Packets):
        for index in range(1,len(self.Default_Cycles_array)):  # For each sub-array (index of sub-array) in the multi dimensional array
            # if index>0: # We dont have to do any changes for the first sub-array
                # print(f"In With Backtrack function-> Current index of cycle is {index}")
            self.T = self.T-1 # Reducing T      # Could be written as self.T *= self.alpha
            self.iteration += 1 # Increasing Iteration
            print(f"Sequence from With_Backtrack function with Reduced Temperature = {self.T} and Iteration number {self.iteration}")
            for inner_index in range(0,len(self.Default_Cycles_array[index])):    # For each index of packet in each cycle/Sub-array
                # print(f"In With_Backtrack function-> packet in 2nd for loop at inner index {inner_index}")
                # Temp_Default_Array = [[]*self.n for i in range(3)]
                Temp_Default_Array = copy.deepcopy(self.Default_Cycles_array)
                # print(f"In With_Backtrack function-> Temp Default array is again set to default as {Temp_Default_Array}")
                temp_packet = Temp_Default_Array[index][inner_index]
                Temp_Default_Array[index-1].append(temp_packet)
                # print(f"In With_Backtrack function-> Added {temp_packet} in cycle {index-1}")
                Temp_Default_Array[index].remove(temp_packet)
                # print(f"In With_Backtrack function-> Removed {temp_packet} in cycle {index}")
                # print(f"In Default function-> Updated Final_array is {self.Default_Cycles_array}")
                self.Final_Array_Of_Valid_Sequences[self.Final_Array_Index] = Temp_Default_Array
                self.Final_Array_Index = self.Final_Array_Index+1
        print(f"In With_Backtrack function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")
        # print(f"In With_Backtrack function-> Updated Final_array_Index is {self.Final_Array_Index}")
        self.With_BackTrack_Flag = 1


    def Without_Backtrack(self,Packets):

        Temp_Default_Array = copy.deepcopy(self.Default_Cycles_array)
        # print(f"In Without_Backtrack function-> Temp Default array initially is {Temp_Default_Array}")
        for index in range(1,len(self.Default_Cycles_array)):  # For each sub-array (index of sub-array) in the multi dimensional array
            self.T = self.T-1 # Reducing T      # Could be written as self.T *= self.alpha
            self.iteration += 1 # Increasing Iteration
            print(f"Sequence from Without_Backtrack function with Reduced Temperature = {self.T} and Iteration number {self.iteration}")

            for inner_index in range(0,len(self.Default_Cycles_array[index])):    # For each index of packet in each cycle/Sub-array

                temp_packet = Temp_Default_Array[index][0]
                # print(f"current temp_packet is {temp_packet}")
                Temp_Default_Array[index-1].append(temp_packet)
                Temp_Default_Array[index].remove(temp_packet)
                # print(f"Final_Array_Index is {self.Final_Array_Index}")
                # print(f"Temp_Default_Array is {Temp_Default_Array}")
                self.Final_Array_Of_Valid_Sequences[self.Final_Array_Index] = Temp_Default_Array
                Temp_Default_Array = copy.deepcopy(self.Final_Array_Of_Valid_Sequences[self.Final_Array_Index])
                self.Final_Array_Index+=1
                # print(f"In Without_Backtrack function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")
        print(f"In Without_Backtrack function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")
        # print(f"In Without_Backtrack function-> Updated Final_array_Index is {self.Final_Array_Index}")
        self.Without_BackTrack_Flag = 1

    def p_accept(self, average_congestion):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(average_congestion - self.least_average_congestion) / self.T)


    def Calculate_Congestion(self, Cycles_array):
        # Total congestion of the sequence is decided as per the length of each cycle
        # and the no. of elements in all cycles after 1st cycle due to congestion created by 1st cycle packets
        peak_congestion = 0
        Sum_Of_congestion = 0
        if Cycles_array:
            for i in range(0, len(Cycles_array)):
                if i == 0:
                    peak_congestion = len(Cycles_array[i])
                    Sum_Of_congestion += len(Cycles_array[i])
                else:                                           # If i!=0 .i.e. if it is 2nd cycle or after that
                    Sum_Of_congestion += len(Cycles_array[i])
                    if len(Cycles_array[i]) > peak_congestion:
                        peak_congestion = len(Cycles_array[i])
            average_congestion = Sum_Of_congestion/(self.highest_constraint)    # Average congestion of a sequence = Sum of packets in the sequence/ Number of cycles
            print(f"Average congestion is {average_congestion}")
            print(f"Peak congestion is {peak_congestion}")
            return peak_congestion, average_congestion
        else:
            pass

    def Simulated_Anneal(self):

        Sorted_Values = []
        for i in self.Sorted_Dict.keys():
            if self.Sorted_Dict[i] not in Sorted_Values:
                Sorted_Values.append(self.Sorted_Dict[i])
        Sorted_Values.sort()
        print(f"Sorted values list is : {Sorted_Values}")
        self.highest_constraint = Sorted_Values[-1]
        lowest_constraint = Sorted_Values[0]
        print(f"Highest constraint within all packets is {self.highest_constraint}") # To create a multi-dimensional array with column = Max number of constraints that a packet can have
        print(f"Lowest constraint within all packets is {lowest_constraint}")

        # Format of multi dim array command -> [[]*Columns for i in range(Rows OR Sub-Arrays)]
        self.Default_Cycles_array =[[]*self.n for i in range(self.highest_constraint)]

        self.Cycles_array =[[]*self.n for i in range(self.highest_constraint)]   # Created multi-dimensional array in which each row represents one cycle of the optimizer
        self.Final_Array_Of_Valid_Sequences = [[]*40 for i in range(40)]

        #Call the default function first->  Get 1 valid sequence first

        self.Find_Default_Sequence(self.Packets)
        # Loop to get all valid sequences
        print("\nStarting Simulated Annealing.")
        while self.T >= self.stopping_temperature and self.iteration <= self.stopping_iter and self.Without_BackTrack_Flag != 1: #
            print(f"T = {self.T} and iteration number {self.iteration}")

            # for i in range(0,len(self.Default_Cycles_array)):
            self.With_BackTrack(self.Packets)

            if self.With_BackTrack_Flag == 1:
                self.Without_Backtrack(self.Packets)

        # # Print the Final array of all valid sequences in rows
        # print(f"In Without_Backtrack function-> Updated Final_array is {self.Final_Array_Of_Valid_Sequences}")

        #Call function to calculate Congestion in the sequence
        for sequence in self.Final_Array_Of_Valid_Sequences:
            if sequence:
                print(f"Current sequence in consideration is {sequence}")
                temp_peak_congestion, temp_average_congestion = self.Calculate_Congestion(sequence)

                if self.second_least_peak_congestion == 0 and self.least_peak_congestion == 0:  # Initialize all values for the first loop as no value would be smaller than 0.
                    self.second_best_sequence = sequence
                    self.second_least_peak_congestion = temp_peak_congestion
                    self.second_least_average_congestion = temp_average_congestion
                    self.best_sequence = sequence
                    self.least_peak_congestion = temp_peak_congestion
                    self.least_average_congestion = temp_average_congestion

                if temp_peak_congestion < self.second_least_peak_congestion or temp_average_congestion < self.second_least_average_congestion:     # comparing with local minima
                    self.second_best_sequence = sequence
                    self.second_least_peak_congestion = temp_peak_congestion
                    self.second_least_average_congestion = temp_average_congestion
                    if temp_peak_congestion < self.least_peak_congestion or temp_average_congestion < self.least_average_congestion:   # Comparing with the least congestion found till now
                        # print("Inside Second if loop")
                        # print(f"Initial least_peak_congestion is {self.least_peak_congestion}")
                        # print(f"Initial least_average_congestion is {self.least_average_congestion}")
                        self.best_sequence = sequence
                        self.least_peak_congestion = temp_peak_congestion
                        self.least_average_congestion = temp_average_congestion
                else:
                    if random.random() < self.p_accept(temp_average_congestion):
                        # print("Inside Else loop")
                        self.second_best_sequence = sequence
                        self.second_least_peak_congestion = temp_peak_congestion
                        self.second_least_average_congestion = temp_average_congestion
                        # print(f"Initial second_least_peak_congestion is {self.second_least_peak_congestion}")
                        # print(f"Initial second_least_average_congestion is {self.second_least_average_congestion}")
        print("\n")
        print(f"Best Sequence obtained: {self.best_sequence}")
        print(f"Least Peak Congestion: {self.least_peak_congestion}")
        print(f"Least Average Congestion: {self.least_average_congestion}")

        return self.best_sequence, self.least_peak_congestion, self.least_average_congestion

        # improvement = 100 * (self.Reprioritized_SequenceOfPackets[0] - self.best_fitness) / (self.Reprioritized_SequenceOfPackets[0])
        # print(f"Improvement over greedy heuristic: {improvement : .2f}%")



# def Get_Packets():      # Consider an array for now and later chnage it to read arbitration IDs of each use case [1]th index of each row in multi dim array
#     Packets = [5, 6, 7, 8, 9]
#     return Packets

# if __name__ == "__main__":
#     Packets = Get_Packets()
#     ##### OR -> Considering scenario in which we have fixed constraints
#     dict = {5:2, 6:1, 7:2, 8:3, 9:2}
#
#     Sorted_Dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
#     print(f'Sorted Dictionary is {Sorted_Dict}')
#
#     sa = SimAnneal(Packets, Sorted_Dict)
#     sa.Simulated_Anneal()
    # sa.visualize_routes()
    # sa.plot_learning()






    # def batch_anneal(self, times=10):
    #     """
    #     Execute simulated annealing algorithm `times` times, with random initial solutions.
    #     """
    #     for i in range(1, times + 1):
    #         print(f"Iteration {i}/{times} -------------------------------")
    #         self.T = self.T_save
    #         self.iteration = 1
    #         self.cur_solution, self.cur_fitness = self.initial_sequence()
    #         self.anneal()

    # def Find_Sequence(self, pack):
    #     max_cycle = self.Sorted_Dict[pack]
    #     print("----------------------------------------------------------")
    #     print(f"Maximum cycle for this loop is {max_cycle}")
    #     # check between Cycles_array[0] till Cycles_array[max_cycle-1] which one has less packets
    #     # for temp_cycle in range(Cycles_array[0], Cycles_array[max_cycle-1]):
    #     # minimum_congestion = len(Cycles_array[0])
    #     minimum_congestion = 0
    #     guess_cycle_number = 0
    #     temp_guess_cycle = 0
    #
    #     for i in range(0,(max_cycle)):
    #         print(f'For index of cycle number equal to {i}')
    #         if minimum_congestion == 0:
    #             minimum_congestion = len(self.Cycles_array[i])
    #             print(f"Minimum congestion for 1st cycle is {minimum_congestion}")
    #         if len(self.Cycles_array[i]) < minimum_congestion:
    #             minimum_congestion = len(self.Cycles_array[i])
    #             print(f"Length of cycle {self.Cycles_array[i]} is {len(self.Cycles_array[i])}")
    #             print(f"Minimum congestion for subsequent cycles is {minimum_congestion}")
    #             print("-----------------")
    #             temp_guess_cycle = i
    #             print(f"Temp Guess cycle is {temp_guess_cycle}")
    #         guess_cycle_number = temp_guess_cycle
    #     print(f"Guess cycle is {guess_cycle_number}")
    #     self.Cycles_array[guess_cycle_number].append(pack)
    #     print("----------------------------------------------------------")
    #
    # def Calculate_Congestion(self, Cycles_array):
    # # Total congestion of the sequence is decided as per the length of each cycle
    # # and the no. of elements in all cycles after 1st cycle due to congestion created by 1st cycle packets
    #     peak_congestion = 0
    #     Sum_Of_congestion = 0
    #     for i in range(0, len(Cycles_array)-1):
    #         if i == 0:
    #             peak_congestion = len(Cycles_array[i])
    #             Sum_Of_congestion += len(Cycles_array[i])
    #         else:                                           # If i!=0 .i.e. if it is 2nd cycle or after that
    #             Sum_Of_congestion += len(Cycles_array[i])
    #             if len(Cycles_array[i]) > peak_congestion:
    #                 peak_congestion = len(Cycles_array[i])
    #     average_congestion = Sum_Of_congestion/(self.highest_constraint)    # Average congestion of a sequence = Sum of packets in the sequence/ Number of cycles
    #     print(f"Average congestion is {average_congestion}")
    #     print(f"Peak congestion is {peak_congestion}")
    #     return peak_congestion, average_congestion
    #
    # #### Function to find initial solution OR make first choice for simulated annealing
    # def initial_sequence(self, Sorted_Values):
    #     """
    #     Greedy algorithm to get an initial solution (closest-neighbour).
    #     """
    #     # Navigate through Sorted values list to decide the range of cycles in which packet is allowed to transmit
    #     Sorted_Values_Index = 0
    #     for pack in self.Sorted_Dict.keys():
    #         print(f"Current packet is {pack}")
    #         # If the constraint is 1
    #         if self.Sorted_Dict[pack] == 1:
    #             self.Cycles_array[0].append(pack)
    #             Sorted_Values_Index = 1
    #             print(f'Next Index in values list is {Sorted_Values_Index}')
    #             print(f'Packet to be finished in 1st cycle {pack}')
    #             print("----------------------------------------------------------")
    #         # For packets whose constraint is other than 1
    #         # This if loop will cover all the packets with the same values/constraint-> will not check if the constraint changes
    #         elif self.Sorted_Dict[pack] == Sorted_Values[Sorted_Values_Index]: # For the packets whose constraint = Current element in Sorted _Values array
    #             self.Find_Sequence(pack)
    #         else:
    #             print(f"Entering the Else section")
    #             Sorted_Values_Index = Sorted_Values_Index+1 # To move to next constraint and look for those packets in next loop
    #             print(f"Updating the Constraint to {Sorted_Values_Index}")
    #             self.Find_Sequence(pack)
    #
    #     print(f'Initial Optimized sequence for Dictionary {self.Sorted_Dict} is:')
    #     print(f"Initial Cycles list/Sequence is {self.Cycles_array}")
    #
    #     #Call function to calculate Congestion in the sequence
    #     peak_congestion, future_congestion = self.Calculate_Congestion(self.Cycles_array)
    #     return self.Cycles_array, peak_congestion, future_congestion
    #
    # def p_accept(self, candidate_fitness):
    #     """
    #     Probability of accepting if the candidate is worse than current.
    #     Depends on the current temperature and difference between candidate and current.
    #     """
    #     return math.exp(-abs(candidate_fitness - self.Current_Congestion) / self.T)
    #
    # def accept(self, candidate):
    #     """
    #     Accept with probability 1 if candidate is better than current.
    #     Accept with probabilty p_accept(..) if candidate is worse.
    #     """
    #
    #     candidate_congestion = self.fitness(candidate)
    #     if candidate_congestion < self.Current_Congestion:
    #         self.Current_Congestion, self.Current_Sequence = candidate_congestion, candidate
    #         if candidate_congestion < self.least_congestion:
    #             self.least_congestion, self.best_sequence = candidate_congestion, candidate
    #     else:
    #         if random.random() < self.p_accept(candidate_congestion):
    #             self.Current_Congestion, self.Current_Sequence = candidate_congestion, candidate
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
