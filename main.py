import os
import sys
import subprocess
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for better UI
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + "\tCloud Backup Manager")

    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "[1] Create Backup and Upload to Cloud")
    print(Fore.BLUE + "[2] Restore Database from Cloud")
    print(Fore.RED + "[3] Delete Backup Data on Cloud")
    print(Fore.MAGENTA + "[4] Exit" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def run_script(option):
    scripts = {
        "1": "clouddump.py",
        "2": "restoration.py",
        "3": "cloudsweep.py"
    }
    
    script_name = scripts.get(option)
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(Fore.RED + f"Error: {script_name} not found in root directory!" + Style.RESET_ALL)
        sys.exit(1)
    
    command = [sys.executable, script_path, '-v']
    subprocess.run(command)

def main():
    while True:
        print_menu()
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
        
        if choice in ["1", "2", "3"]:
            run_script(choice)
        elif choice == "4":
            print(Fore.CYAN + "Exiting Cloud Backup Manager. Goodbye!" + Style.RESET_ALL)
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice! Please enter a number between 1 and 4." + Style.RESET_ALL)
        
        input(Fore.MAGENTA + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()