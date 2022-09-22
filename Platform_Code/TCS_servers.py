import subprocess


def TCS_Servers_Main():
	print("----------------------------------------In TCS_Servers.py------------------------------------------")
	subprocess.run("python3 TCS_recv.py & python3 TCS_process.py & python3 ECM.py & python3 Instrument_cluster.py", shell=True)
	
	
if __name__ == '__main__' :
    TCS_Servers_Main()




