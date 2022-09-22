import subprocess

def RT_Servers_Main():
	print("----------------------------------------In RT_Servers.py------------------------------------------")
	subprocess.run("python3 EPS_recv.py & python3 EPS_process.py & python3 Assist_motor.py & python3 Load_motor.py", shell=True)
	
	
if __name__ == '__main__' :
    RT_Servers_Main()




