import os
import pyfiglet
import subprocess
from colorama import Fore, Style, init
from InteractiveMode import run_IA_model
from AnalysisMode import run_analysis_mode
from Utils import intial_log
#from Config import MODEL_DIR

# Initialize colorama
init(autoreset=True)

# Function to center text based on a fixed width
def center_text_fixed(text, width, color=Fore.YELLOW):
    return f"{color}{text.center(width)}{Style.RESET_ALL}"

# ASCII Banner (Left-Aligned, Green)
ascii_banner = """
 █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗    ██╗███╗   ██╗████████╗███████╗██╗     ██╗     ██╗ ██████╗ ███████╗███╗   ██╗ ██████╗███████╗
██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ██║████╗  ██║╚══██╔══╝██╔════╝██║     ██║     ██║██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝
███████║   ██║      ██║   ███████║██║     █████╔╝     ██║██╔██╗ ██║   ██║   █████╗  ██║     ██║     ██║██║  ███╗█████╗  ██╔██╗ ██║██║     █████╗  
██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗     ██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██║     ██║██║   ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  
██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗    ██║██║ ╚████║   ██║   ███████╗███████╗███████╗██║╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗
╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
"""

# Fixed width based on ASCII banner
BANNER_WIDTH = 146  # Adjust this based on ASCII art width

# Centered Disclaimers under ASCII Banner
disclaimer_1 = center_text_fixed("!! Disclaimer: This tool is not meant for unethical usage !!", BANNER_WIDTH, Fore.RED)
disclaimer_2 = center_text_fixed("!! Creators of this tool are not held responsible for unethical practices !!", BANNER_WIDTH, Fore.RED)

#Centered Info
info_text = center_text_fixed(".:: AI Powered Automation Penetration Testing Tool ::.", BANNER_WIDTH, Fore.LIGHTYELLOW_EX)
developer_text = center_text_fixed(".:: Developed by Embry-Riddle Students in Association with Boeing ::.", BANNER_WIDTH, Fore.LIGHTYELLOW_EX)

# Divider bars (Same length as ASCII art width)
block_divider = center_text_fixed("=" * BANNER_WIDTH, BANNER_WIDTH, Fore.BLUE)
menu=pyfiglet.figlet_format("MENU")
# Enlarged Menu Label (Green, Left-Aligned)
menu_title = Fore.LIGHTYELLOW_EX + menu + Style.RESET_ALL

# Default AI Model
selected_model = "WhiteRabbitNeo"

#Model Directory
#MODEL_DIR = "/home/mlserver/BC/Models"
# Menu options
menu_options = {
    "1": "Run AI Powered Interactive Scan",
    "2": "Generate Pen Test Report",
    "3": "Export Findings",
    "4": "Change AI Model",
    "5": "Exit"
}
def list_models():
    print("\nALL AVALIABLE MODELS\n")
    try:
        models = [f for f in os.listdir(MODEL_DIR) if f.endswith(".gguf")]
        if not models:
            print("No .gguf models found with that name\n")
            return none
        for idx, model in enumerate(models, start=1):
            print(f"[{idx}]{model}")
        return models
    except FileNotFoundError:
        print("Model Directory not Found 404\n")
        return none

def switch_model():
    models = list_models()
    if not models:
        return none
    choice = input("\nEnter the Number of the model you want to use:")
    if choice.isdigit():
        choice = int(choice) - 1
        if 0 <= choice < len(models):
            selected_model = models[choice]
            print(f"\n Switching to Model: {selected_model}\n")
            return os.path.join(MODEL_DIR, selected_model)
        else:
            print("Invalid Selection")
            return none
    else:
        print("Please enter a Valid Number")
        return none


def display_menu():
    os.system("clear" if os.name == "posix" else "cls")  # Clears terminal for a fresh display

    # Display ASCII Banner (Left-Aligned)
    print(Fore.YELLOW + ascii_banner + Style.RESET_ALL)

    # Centered Disclaimer and Dividers BELOW the ASCII Banner
    print(block_divider)
    print(info_text)
    print(developer_text)
    print(block_divider)  
    print(disclaimer_1)
    print(disclaimer_2)
    print(block_divider + "\n")  

    # Enlarged Menu Title (Below ASCII Banner)
    #print(menu_title)
    #print(block_divider)
    print(f"Current AI Platform: {Fore.MAGENTA}GPT4All{Style.RESET_ALL}\n")
    print(f"Current AI Model: {Fore.CYAN}{selected_model}{Style.RESET_ALL}\n")  # Show selected AI model
    
    # Display Menu Options
    for key, value in menu_options.items():
        if key == "5":
            print(f"[{Fore.RED}{key}{Style.RESET_ALL}] {Fore.RED}{value}{Style.RESET_ALL}")  # Exit in Red
        elif key == "4":
            print(f"[{Fore.LIGHTYELLOW_EX}{key}{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}{value}{Style.RESET_ALL}")  # Change AI Model in Yellow
        else:
            print(f"[{Fore.LIGHTWHITE_EX}{key}{Style.RESET_ALL}] {Fore.LIGHTWHITE_EX}{value}{Style.RESET_ALL}")

    print("\n")  

def main():
    
    global selected_model  # Allow modification of the model name
    while True:
        display_menu()
        intial_log()
        choice = input(Fore.LIGHTWHITE_EX + "Select an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            print(Fore.LIGHTWHITE_EX + "\nStarting AI Powered Interactive Shell\n" + Style.RESET_ALL)
            run_IA_model()
        elif choice == "2":
            print(Fore.LIGHTWHITE_EX + "\nRunning Analysis Mode...\n" + Style.RESET_ALL)
            run_analysis_mode()
        elif choice == "3":
            print(Fore.LIGHTWHITE_EX + "\nWrite Report...\n" + Style.RESET_ALL)
            #write report function
        elif choice == "4":
            selected_model = switch_model()
        elif choice == "5":
            print(Fore.RED + "\nExiting... Goodbye!\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nInvalid option! Please select again.\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
