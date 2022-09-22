import subprocess

subprocess.run("python3 TCS_clients.py & python3 ABS_clients.py & python3 RT_clients.py", shell=True)
