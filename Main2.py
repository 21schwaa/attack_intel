import subprocess
import re
import textwrap
import datetime
import time
import shlex
from gpt4all import GPT4All

#===============================================================================================

#Define the Files called in Functions
Log_File = "testsessionlog.txt"
WHITELIST_FILE = "/home/mlserver/BC/Whitelists/cmd_whitelist.txt"
#GREYLIST_FILE = "NO FILE CREATED YET"
PROMPT="/home/mlserver/BC/Prompts/system_prompt3.txt"
PROMPT2="/home/mlserver/BC/Prompts/system_prompt2.txt"

#===============================================================================================

def load_whitelist(filename):
    try:
        with open(filename, "r", encoding="utf-8")as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        print(f"Warning {filename} not found! No commands will be whitelisted.")
        return set()

#===============================================================================================

#Command Lists (need to add grey list file soon)
WHITELIST = load_whitelist(WHITELIST_FILE)
#GREYLIST = load_greylist(GREYLIST_FILE)

#===============================================================================================

#creating the log session function
def log_session(user_question, raw_command, cleaned_command, output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M:%s")

    log_entry = (
            f"\n[{timestamp}]\n"
            f"User Asked: {user_question}\n"
            f"AI Raw Output: {raw_command}\n"
            f"Cleaned Command: {cleaned_command}\n"
            f"Command Ouput:\n{output}\n"
            f"{'-'*40}\n"
    )
    with open(Log_File, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

#=============================================================================================

#function to clean output
def clean_command(command):
    command = command.strip() #remove extra space
    command = re.sub(r"^```[a-zA-Z]*\n?","",command) #Removes any opening statement
    command = re.sub(r"\n?```$","", command) #Removes Closing Statement

    #remove excessive indentation
    command = textwrap.dedent(command)

    #normalize spaces
    command = re.sub(r"\s+"," ",command).strip()

    #remove pipes
    command = command.split("|")[0].strip()


    return command.strip()

#========================================================================================================================================================

#Load system Prompt
def load_system_prompt():
    try:
        with open(PROMPT,"r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: Sysem prompt file no found at {PROMPT}. Using Default Prompts")
        return "system_prompt.txt"

#=========================================================================================================================================================


#Load system Prompt 2
#def load_system_prompt2():
 #   try:
 #
 #with open(PROMPT2,"r", encoding="etf-8") as file:
 #           return file.read().strip()
  #  except FileNotFoundError:
   #     print(f"Warning: System prompt file no found {PROMPT2}. Using Defualt Prompts")
    #    return "system_prompt2.txt"


#=========================================================================================================================================================


# Function to Run terminal commands with restraint
def run_command(command):
    cmd_parts = shlex.split(command)
    cmd_name = cmd_parts[0] if cmd_parts else ""
    
    if cmd_name in WHITELIST:
        try:
            result = subprocess.run(cmd_parts, text=True, capture_output=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e), "Execution Failed"
   # elif cmd_name in GREYLIST:
    #    confirmantion = input(f"Command '{command}' is in the greylist.Possible unethical or damages to machine. EXECUTE? (yes/no):".strip().lower()
     #   if confirmation == "yes"
      #      try:
       #         result = subprocess.run(cmd_parts, text=True, capture_output=True)
        #        return result.stdout if result.stdout else result.stderr
         #   except Exception as e:
          #      return str(e), "Execution Failed (Confirmed)"
       # else:
        #    return "Execution Denied By User", "Denied"
    else:
        return "Denied", "Command not allowed for Security Reasons.", "To Allow this command Please add it to either the WHITELIST or GREYLIST"

#=========================================================================================================================================================

#Load model
print("\n LOADING MODEL\n")
time.sleep(3)
model = GPT4All("whiterabbitneo-13b.Q8_0.gguf")
print("MODEL SUCESS\n")

#============================================================================================================

#Intro
print("\n WELCOME TO ATTACK INTEL INTERACTIVE PROMPT: Type exit to quit\n")

while True:
   # print("Please Wait While The model is Being Fed Prompts\n")
    user_question = input("Ask the Model To Perform a task!\nRemember the more info you give the better!\n")
    if user_question.lower() in ["exit","quit"]:
        print("Returning to Main Menu: All Entries Saved to Log File\n")
        break
    #Feed the system prompt
    system_prompt = load_system_prompt()
   # system_prompt2 = load_system_prompt2()

    #Generate a Command with the  model
    with model.chat_session():
        raw_command = model.generate("Please provide a Linux command related to the following security situation: " + user_question + ", provide only a Linux command that addresses the situation. Respond with notheing but the command, no explanations or additional text.", max_tokens=20).strip()
        command = clean_command(raw_command)
        if command:
            print(f"Generated Command: {command.strip()}")
            #Run the Command and Store Output
            output = run_command(command.strip())
            #Print Command Output
            print(f"Command Output:\n{output}")

        else:
            print(f"Command Output:\n{output}")

    log_session(user_question, raw_command, command, output)

    #Ask if user wants to continue
    while True:
        user_continue = input("Would you like to continue?[y/n] ")
        if user_continue.lower() in ["y", "yes"]:
            user_follow_question = input("Ask the Model to perform a follow up task!\nRemember the more info you give the better!\n")
            
            #generate command with the Model
            with model.chat_session():
                raw_command = model.generate("Please provide a Linux command related to the following security situation: " + user_follow_question + " The last command you ran was: " + command + "Do not include any explanations, context, or text outside of the command itself." , max_tokens=20).strip()
                command = clean_command(raw_command)
                if command:
                    print(f"Generated Command: {command.strip()}")
                    #Run the command and store the output
                    output = run_command(command.strip())
                    #print the command output
                    print(f"Command Output:\n{output}")
                else:
                    print(f"Command Output:\n{output}")

            log_session(user_follow_question, raw_command, command, output)
        else:
            break
        
#=============================================================================================================

