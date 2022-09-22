import subprocess


subprocess.run("python3 EPS_process.py & python3 Assist_motor.py & python3 Load_motor.py", shell=True)