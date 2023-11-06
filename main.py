import os
import time

serveur = "serveur_flask.py"

serveur_command = f"py {serveur}"
os.system(f"start cmd /k {serveur_command}")

time.sleep(1)


script_without_gpt = "Script/script_without_gpt.py"

script_command = f"py {script_without_gpt}"
os.system(f"start cmd /k {script_command}")