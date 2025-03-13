import time 
from Models import load_main_model
from Utils import clean_command, run_command, log_session
from Config import load_system_prompt


def run_IA_model():
    #runs the interactive model where the user can ask the model to generate and run commands
    model = load_main_model()

    while True:
        #prompt the user for input 
        user_question = input("\nAsk the model to perform a task!(Type 'exit' to quit\n>")

        if user_question.lower()in ["exit", "quit"]:
            print("Returning to Main Menu: All Entires Saved to Log File\n")
            break
        
        system_prompt = load_system_prompt()


        with model.chat_session():
            raw_command = model.generate(
                    f"{system_prompt}\n\nUser: {user_question}\n\nLinux command: ",
                    max_tokens=20
            ).strip()

        command=clean_command(raw_command)

        if command:
            print(f"\n Generated Command: {command.strip()}")


            output = run_command(command.strip())

            print(f"\nCommand Output:\n{output}")

            log_session(user_question, raw_command, command, output)
        else:
            print("\nno valid command generated")

        while True:
            user_cont = input("\nWould you like to continue? (yes/no)\n>").strip().lower()
            if user_cont in ["y","yes"]:
                break
            elif user_cont in ["n", "no"]:
                return
            else:
                print("invalid input")


