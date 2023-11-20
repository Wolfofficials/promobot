import subprocess
import platform
import os

os_type = platform.system()

script_dir = os.path.dirname(os.path.abspath(__file__))

subprocess.Popen(f'python3 "{os.path.join(script_dir, "join.py")}" &', shell=True)

subprocess.Popen(f'python3 "{os.path.join(script_dir, "spam.py")}" &', shell=True)

subprocess.Popen(f'python3 "{os.path.join(script_dir, "pmpermit.py")}" &', shell=True)

subprocess.Popen(f'python3 "{os.path.join(script_dir, "cmds.py")}" &', shell=True)
