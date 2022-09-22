import subprocess

def All_Clients_Main():
	print("----------------------------------------In ABS_Servers.py------------------------------------------")
	subprocess.run("python3 TCS_clients.py & python3 ABS_clients.py & python3 RT_clients.py", shell=True)
	
if __name__ == '__main__' :
    All_Clients_Main()
