#Analysis Mode Prompt
#This prompt is only for the use of analysis of outputs from the interactive logs.
import os
from Models import load_analysis_model
from Utils import log_session, intial_log, LOG_DIR
from Config import load_system_prompt2



def get_latest_log_content():
    try:
        if not os.path.exists(LOG_DIR):
            return "No Logs Available"


        logs = sorted(os.listdir(LOG_DIR), reverse=True)
        if not logs:
            return "No Logs Available"


        latest_log_path = os.path.join(LOG_DIR, logs[0])
        with open(latest_log_path,"r",encoding="utf-8")as file:
            return file.read()

    except Exception as e:
        return f"Error rerieving log file: {str(e)}"


def run_analysis_mode():
    #runs the analysis mode where the user can request AI Produced analysis
    model = load_analysis_model()

    while True:
        #prompt the user for a question
        user_question = input ("\nEnter your analysis query(Type 'Exit' to return to the main menu):\n>")

        #exit process
        if user_question.lower() in ["exit","quit"]:
            print("Returning to Main Menu")
            break

    
        system_prompt2 = load_system_prompt2()
        log_content = get_latest_log_content()

        full_analysis_input = """{}
User Question: {}

Current Log Data:
{}


Analysis:""".format(system_prompt2,user_question,log_content)


        with model.chat_session():
            #system Prompt 2 needs to be changed to the network sec admin prompt
            #the logs are stored in a  dir

            analysis_output = model.generate(full_analysis_input,max_tokens=330).strip()

#Display Analysis
        print(f"\nAnalysis Output:\n{analysis_output}")

#Log the session 
        log_session(user_question, "N/A" , "N/A", analysis_output)

        #ask the user if they want to continue analysis
        while True:
            user_cont = input("\nWould you linke to continue analysis? (Yes/No)\n>").strip().lower()
            if user_cont in ["y", "yes"]:
                break
            elif user_cont in ["n", "no"]:
                return
            else:
                print("invalid input")

