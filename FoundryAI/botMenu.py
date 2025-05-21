# Script  :  botMenu.py
# Version :  1.0
# Date    :  5/20/25
# Author: Jody Ingram
# Notes: Python-based menu that imports OS settings and Foundry AI Bot and allows bot to run interactive commands.


# foundry_launcher.py

import os
import time
import subprocess

def run_ai_chat():
    # Calls Foundry AI from Batch File
    os.system("start botLauncher.bat")
    
    # os.system("python foundry_model.py") // Use this if calling Foundry AI from another Python file.

def check_uptime():
    uptime = subprocess.check_output("powershell -Command \"(get-date) - (gcim Win32_OperatingSystem).LastBootUpTime\"", shell=True)
    print("System Uptime:", uptime.decode().strip())
    input("Press Enter to return to menu...")

def open_notepad():
    os.system("start notepad")

def exit_program():
    print("Exiting Foundry Launcher...")
    time.sleep(1)
    exit()

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Foundry AI Launcher ===")
        print("1. Talk to Foundry AI Bot")
        print("2. Check System Uptime")
        print("3. Launch Windows Notepad")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            run_ai_chat()
        elif choice == '2':
            check_uptime()
        elif choice == '3':
            open_notepad()
        elif choice == '4':
            exit_program()
        else:
            print("Invalid selection. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
