import datetime
import os
import re
import textwrap
import subprocess
import shlex
import getpass
from Config import WHITELIST, Log_File

LOG_DIR = "/home/mlserver/BC/Logs/"
LOG_FILE = None
LOG_MODE = None
LOG_USER = None

def clean_command(command):
    command = command.strip()
    command = re.sub(r"^```[a-zA-Z]*\n?","",command)
    command = re.sub(r"\n?```$","",command)
    command = re.split(r'(?<=\S)\s*```', command)[0].strip()
    commmad = textwrap.dedent(command)
    command = re.sub(r"\s+", " ",command).strip()
    command = command.split("|")[0].strip()
    return command.strip()

def run_command(command):
    cmd_parts = shlex.split(command)
    cmd_name = cmd_parts[0] if cmd_parts else ""

    if cmd_name in WHITELIST:
        try:
            result = subprocess.run(cmd_parts, text=True, capture_output=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e), "Execution Failed"
    else:
        return "Denied",  "Command not allowed for saftey pleae add to whitelist"

def intial_log():
 
#    """Prompt the user to create a new log file or use the existing one"""
    global LOG_MODE, LOG_FILE, LOG_USER

    LOG_USER = getpass.getuser()
    os.makedirs(LOG_DIR, exist_ok=True)                        

#ensuring the log path exists
    if not os.path.exists(LOG_DIR):
        print("Error No Directory Named {LOG_DIR}")





    while True:
        user_choice = input ("\nWould you like to create a new log file?(yes/no)").strip().lower()

        if user_choice in ["yes", "y"]:
            timestamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%s")
            filename = f"{LOG_USER}_log_{timestamp}.txt"
            LOG_FILE = os.path.join(LOG_DIR, filename)
            LOG_MODE = "w"
            print("New Log File Created at: {LOG_FILE}"

        elif user_choice in ["no", "n"]:
            existing_logs = sorted(os.listdir(LOG_DIR), reverse = True)
            if existing_logs:
                LOG_FILE = os.path.join(LOG_DIR,existing_logs[0])
                print("Appending to the existing log file:{LOG_FILE}")
                LOG_MODE = "a"
            else:
                print("No Exisitng Log File Found, Creating a new one......")
        else:
            print("Invalid Input: Please Type 'Yes' or 'No' ")

def create_log
    #actually writes to log file
    global LOG_FILE, LOG_MODE, LOG_USER
    if not LOG_FILE or not LOG_MODE != "w":
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%s")
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            file.write(f"New log started by {LOG_USER} on {timesamp}\n"
        print(f"Log File created: {LOG_FILE}")


def log_session(user_question,raw_command,cleaned_command,output):
    #Logs user input, AI response, and command exection ouputs"
    global LOG_MODE, LOG_FILE, LOG_USER
    if not LOG_FILE or not LOG_MODE:
        print("Logging has not been initialized.")
        return

    intial_log()


    timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    log_entry = (
            f"\n[{timestamp}] (User: {LOG_USER})\n"
            f"User Asked: {user_question}\n"
            f"AI raw output: {raw_command}\n"
            f"Cleaned Command: {cleaned_command}\n"
            f"Command Output:\n{output}\n"
            f"{'-' * 40}\n"
    )
    with open (LOG_FILE, "a", encoding="utf-8")as log_file:
        log_file.write(log_entry)

