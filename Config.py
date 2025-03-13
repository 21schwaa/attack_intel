#config.py
#this is the main config file that the code will run off of
#here you can change file paths for whitelists, prompts, and logs
import os

#file paths
WHITELIST_FILE = "/home/mlserver/BC/Whitelists/cmd_whitelist.txt"
PROMPT = "/home/mlserver/BC/Prompts/system_prompt3.txt"
PROMPT2 = "/home/mlserver/BC/Prompts/system_prompt2.txt"
Log_File = "testsessionlog.txt"



def load_whitelists(filename):
#loads whitelist
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        print(f"WARNING: {filename} not found! No Commands Will be Whitelisted.")
        return set()

#Load the whitelist at startup 
WHITELIST = load_whitelists(WHITELIST_FILE)

def load_system_prompt():
    #Loads the system prompt from files
    try:
        with open(PROMPT, "r",encoding="utf-8")as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"WARNING: System Prompt file not found at {prompt}. Using Default Prompt.")
        return "Default System Prompt in use"

def load_system_prompt2():
#loads the second prompt optional usage
    try:
        with open(PROMPT2, "r",encoding="utf-8")as file:
            return file.read().strip()
    except FileNotFoundError:
        print("WARNING: Analysis system Prompt not found at {PROMPT2} Using Default Prompt")
        return "Default System Prompt in use"
