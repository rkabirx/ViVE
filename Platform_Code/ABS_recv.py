# ABS use case
# Calls all receiving scripts

print("Receiving from Wheel speed sensor and brake pedal to ABS")
import ABS_process
ABS_process.abs_recv()
print("-----------------------------------------------------------------")


# print("Receiving from ABS to Rack & Pinion")
# import Sim_pressure_recv
# Sim_pressure_recv
