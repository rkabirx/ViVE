import subprocess


subprocess.run("python3 TCS_process.py & python3 ECM_process.py & python3 Instrument_cluster.py", shell=True)

