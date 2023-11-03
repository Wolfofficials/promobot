import subprocess
import platform
import os

# Get the operating system
os_type = platform.system()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Start script1.py
subprocess.Popen(f'python3 "{os.path.join(script_dir, "join.py")}" &', shell=True)

# Start script2.py
subprocess.Popen(f'python3 "{os.path.join(script_dir, "spam.py")}" &', shell=True)

# Start script3.py
subprocess.Popen(f'python3 "{os.path.join(script_dir, "pmpermit.py")}" &', shell=True)
