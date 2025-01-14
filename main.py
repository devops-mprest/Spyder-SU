# Import the modules from the modules.py file
from modules import *
from app_functions import *
from ping import *
import threading
from tkinter import messagebox
import socket
from softwares import *
import os
import datetime

# Functions
# Functions for networking check and threading
def update_progressbar(pb, progress_value):
    pb['value'] = progress_value

def update_softwares_progressbar(pbs, progress_value):
    pbs['value'] = progress_value

def networking(battnumber, project, set, b9, diff_network):
    global pb_label
    global pb
    # Create a progress bar and label
    if set == 'Main+Backup':
        b9.configure(bootstyle='WARNING')
        pb = ttk.Progressbar(root, bootstyle='WARNING', maximum=200, mode="indeterminate", length=200, value=0)
        pb.place(relx=0.73, rely=0.72)
        pb.start(10)
        pb_label = ttk.Label(root, text="Networking Check In Progress")
        pb_label.place(relx=0.68, rely=0.68)
        pb_label.configure(text="Networking Check In Progress")
    else:
        b9.configure(bootstyle='WARNING')
        pb = ttk.Progressbar(root, bootstyle='WARNING', mode="indeterminate", length=100)
        pb.place(relx=0.73, rely=0.72)
        pb.start(10)
        pb_label = ttk.Label(root, text="Networking Check In Progress", background="#000000")
        pb_label.place(relx=0.68, rely=0.68)
        pb_label.configure(text="Networking Check In Progress")

    # Create a thread to run the ping function
    def ping_thread():
        # Run the ping function and get the result
        result = ping(battnumber, project, set, update_progressbar, pb, diff_network)

        # Update the progress bar and label
        if result == 0:
            # update_progressbar(pb, 100)  # Assuming ping success should update to 100%
            messagebox.showinfo("Ping Success", "All pings were successful.")
            b9.configure(bootstyle='SUCCESS')
            pb.stop()
            pb_label.place_forget()
            pb.place_forget()            
        else:
            b9.configure(bootstyle='DANGER')
            pb.stop()
            pb_label.place_forget()
            pb.place_forget()
            messagebox.showerror("Ping Failed", "There failures in the ping test.", icon="error")

    # Start the thread to run the ping function
    threading.Thread(target=ping_thread, daemon=True).start()

def software_check(battnumber,project,set,b10):
    global pbs_label
    global pbs

    def log_error(error_message):
    # Get the current time in a readable format
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Specify the log file path (adjust the path as needed)
        log_file = "softwares_logs.log"

    # Write the error message to the log file
        with open(log_file, 'a') as log:
            log.write(f"[{current_time}] {error_message}\n")
    
    if set == 'Main+Backup':
        remote_computers = [r'\\pc-bene',r'\\MC2',r'\\RC2',r'\\MICS',r'\\RICS',r'\\MDB',r'\\RDB',r'\\OC1',r'\\OC2']
        b10.configure(bootstyle='WARNING')
        pbs = ttk.Progressbar(root, bootstyle='WARNING', mode="indeterminate", length=200)
        pbs.start(10)
        pbs.place(x=450, y=495)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000")
        pbs_label.place(x=450, y=475)
        pbs_label.configure(text="Softwares Check In Progress")
    
        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0
             # Changed search_name to a dictionary with software names as keys and None as placeholders for versions
            search_name = {
                "Microsoft Visual C++ 2022 X64 Additional Runtime - 14.42.34433": "14.42.34433",
                "7-Zip": "24.09",
                "Npcap": "0.9994",
                "Google Chrome": "131.0.6778.265",
                "Microsoft Visual C++ 2015-2022 Redistributable x64": "14.36.32532.0",
                "Microsoft Visual C++ 2015-2022 Redistributable x86": "14.36.32532.0",
                "Notepad++": "7.8.2",
                "Meinberg": "4.2.4p6",
                "Moxa": "3.0",
                "Screen presser": "4.0"
            }
            # Query the remote registry                 
            for computer in remote_computers:
                helper = 0
                if computer == "\\\\pc-bene":
                    softwares_numbers = 10
                    search_name = {
                    "Npcap": "0.9994",                       
                    "Microsoft Visual C++ 2022 X64 Additional Runtime - 14.42.34433": "14.42.34433",
                    "7-Zip": "24.09",
                    "Google Chrome": "131.0.6778.265",
                    "Microsoft Visual C++ 2015-2022 Redistributable x64": "14.36.32532.0",
                    "Microsoft Visual C++ 2015-2022 Redistributable x86": "14.36.32532.0",
                    "Notepad++": "7.8.2",
                    "Meinberg": "4.2.4p6",
                    "Moxa": "3.0",
                    "Screen presser": "4.0"
                    }
                for software, version in search_name.items():  # Iterate through the dictionary
                    results = query_remote_registry(computer, registry_path_one, software)
                    if results == "[WinError 53] The network path was not found":
                        log_message = f"[WinError 53] The network path was not found for {computer}"
                        log_error(log_message)  
                    elif results:
                        for result in results:
                            software_version = result.get('DisplayVersion')
                            software_name = result.get('DisplayName')
                            if software_name == software and software_version == version:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                log_error(log_message)
                                helper += 1
                            else:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                log_error(log_message)                                                               
                    elif results:
                        # If no result from the first path, query the second registry path
                        results = query_remote_registry(computer, registry_path_two, software)
                        if results:
                            for result in results:
                                software_version = result.get('DisplayVersion')
                                if software_version == version:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                    log_error(log_message)
                                    helper += 1
                                else:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                    log_error(log_message)          
                    else:
                            print(f"DisplayName: {software}, DisplayVersion: {version}")
                            log_message = f"ERROR: {software} {version} not Installed on {computer}"
                            log_error(log_message)
                if helper == softwares_numbers:
                    compare_main_result += 1
                    messagebox.showWARNING('Softwares', f"{computer} have all of the softwares installed" )
                    log_message = f"SUCCESS: {computer} have all of the softwares installed"
                    log_error(log_message) 
                else:
                    messagebox.showerror('Softwares', f"{computer} have {helper} of {softwares_numbers} softwares installed" )
                    log_message = f"ERROR: {computer} have {helper} of {softwares_numbers} softwares installed"
                    log_error(log_message)                                     

            if main_result == compare_main_result:
                b10.configure(bootstyle='SUCCESS')
                pbs.stop()
                pbs.place_forget
                pbs_label.place_forget
            else:
                b10.configure(bootstyle='DANGER')
                pbs.stop()
                pbs.place_forget()
                pbs_label.place_forget()
                
        # Start the threading
        threading.Thread(target=software_thread, daemon=True).start()
    elif set == 'Main':
        remote_computers = [r'\\pc-bene',r'\\MC2',r'\\MICS',r'\\MDB',r'\\OC1']
        b10.configure(bootstyle='WARNING')
        pbs = ttk.Progressbar(root, bootstyle='WARNING', mode="indeterminate", length=100)
        pbs.start(10)
        pbs.place(relx=0.73, rely=0.79)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000")
        pbs_label.place(relx=0.68, rely=0.75)
        pbs_label.configure(text="Softwares Check In Progress")
    
        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0
             # Changed search_name to a dictionary with software names as keys and None as placeholders for versions
            search_name = {
                "Microsoft Visual C++ 2022 X64 Additional Runtime - 14.42.34433": "14.42.34433",
                "7-Zip": "24.09",
                "Npcap": "0.9994",
                "Google Chrome": "131.0.6778.265",
                "Microsoft Visual C++ 2015-2022 Redistributable x64": "14.36.32532.0",
                "Microsoft Visual C++ 2015-2022 Redistributable x86": "14.36.32532.0",
                "Notepad++": "7.8.2",
                "Meinberg": "4.2.4p6",
                "Moxa": "3.0",
                "Screen presser": "4.0"
            }
            # Query the remote registry                 
            for computer in remote_computers:
                helper = 0
                if computer == "\\\\pc-bene":
                    softwares_numbers = 10
                    search_name = {
                    "Npcap": "0.9994",                       
                    "Network Time Protocol": "4.2.4p6@vegas-v2-o-custom",
                    "NTP Time Server Monitor 1.04": "0.9g",
                    "Google Chrome": "131.0.6778.265",
                    "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127": "14.24.28127",
                    "Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.26.28720": "14.26.28720.3",
                    "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161": "9.0.30729.6161",
                    "Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.24.28127": "14.24.28127.4",
                    "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127": "14.24.28127",
                    "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161": "9.0.30729.6161",
                    "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219": "10.0.40219",
                    "MOXA Smartio/Industio Windows Driver Ver3.1": "3.1",
                    "7-Zip 9.20 (x64 edition)": "9.20.00.0",
                    "Notepad++ (64-bit x64)": "7.8.4",
                    }           
                if computer == "\\\\MC2":
                    softwares_numbers = 10
                    search_name = {
                    "Npcap": "0.9994",                       
                    "Network Time Protocol": "4.2.4p6@vegas-v2-o-custom",
                    "NTP Time Server Monitor 1.04": "0.9g",
                    "Google Chrome": "131.0.6778.265",
                    "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127": "14.24.28127",
                    "Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.26.28720": "14.26.28720.3",
                    "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161": "9.0.30729.6161",
                    "Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.24.28127": "14.24.28127.4",
                    "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127": "14.24.28127",
                    "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161": "9.0.30729.6161",
                    "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219": "10.0.40219",
                    "MOXA Smartio/Industio Windows Driver Ver3.1": "3.1",
                    "7-Zip 9.20 (x64 edition)": "9.20.00.0",
                    "Notepad++ (64-bit x64)": "7.8.4",
                    }                    
                for software, version in search_name.items():  # Iterate through the dictionary
                    results = query_remote_registry(computer, registry_path_one, software)
                    if results == "[WinError 53] The network path was not found":
                        log_message = f"[WinError 53] The network path was not found for {computer}"
                        log_error(log_message)  
                    elif results:
                        for result in results:
                            software_version = result.get('DisplayVersion')
                            software_name = result.get('DisplayName')
                            if software_name == software and software_version == version:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                log_error(log_message)
                                helper += 1
                            else:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                log_error(log_message)                                                               
                    elif results:
                        # If no result from the first path, query the second registry path
                        results = query_remote_registry(computer, registry_path_two, software)
                        if results:
                            for result in results:
                                software_version = result.get('DisplayVersion')
                                if software_version == version:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                    log_error(log_message)
                                    helper += 1
                                else:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                    log_error(log_message)          
                    else:
                            print(f"DisplayName: {software}, DisplayVersion: {version}")
                            log_message = f"ERROR: {software} {version} not Installed on {computer}"
                            log_error(log_message)
                if helper == softwares_numbers:
                    compare_main_result += 1
                    messagebox.showWARNING('Softwares', f"{computer} have all of the softwares installed" )
                    log_message = f"SUCCESS: {computer} have all of the softwares installed"
                    log_error(log_message) 
                else:
                    messagebox.showerror('Softwares', f"{computer} have {helper} of {softwares_numbers} softwares installed" )
                    log_message = f"ERROR: {computer} have {helper} of {softwares_numbers} softwares installed"
                    log_error(log_message)                                     

            if main_result == compare_main_result:
                b10.configure(bootstyle='SUCCESS')
                pbs.stop()
                pbs.place_forget
                pbs_label.place_forget
            else:
                b10.configure(bootstyle='DANGER')
                pbs.stop()
                pbs.place_forget()
                pbs_label.place_forget()
                
        # Start the threading
        threading.Thread(target=software_thread, daemon=True).start()

    elif set == 'Backup':
        remote_computers = [r'\\pc-bene',r'\\RC2',r'\\RICS',r'\\RDB',r'\\OC2']
        b10.configure(bootstyle='WARNING')
        pbs = ttk.Progressbar(root, bootstyle='WARNING', mode="indeterminate", length=200)
        pbs.start(10)
        pbs.place(x=450, y=495)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000")
        pbs_label.place(x=450, y=475)
        pbs_label.configure(text="Softwares Check In Progress")
    
        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0
             # Changed search_name to a dictionary with software names as keys and None as placeholders for versions
            search_name = {
                "Microsoft Visual C++ 2022 X64 Additional Runtime - 14.42.34433": "14.42.34433",
                "7-Zip": "24.09",
                "Npcap": "0.9994",
                "Google Chrome": "131.0.6778.265",
                "Microsoft Visual C++ 2015-2022 Redistributable x64": "14.36.32532.0",
                "Microsoft Visual C++ 2015-2022 Redistributable x86": "14.36.32532.0",
                "Notepad++": "7.8.2",
                "Meinberg": "4.2.4p6",
                "Moxa": "3.0",
                "Screen presser": "4.0"
            }
            # Query the remote registry                 
            for computer in remote_computers:
                helper = 0
                if computer == "\\\\pc-bene":
                    softwares_numbers = 10
                    search_name = {
                    "Npcap": "0.9994",                       
                    "Microsoft Visual C++ 2022 X64 Additional Runtime - 14.42.34433": "14.42.34433",
                    "7-Zip": "24.09",
                    "Google Chrome": "131.0.6778.265",
                    "Microsoft Visual C++ 2015-2022 Redistributable x64": "14.36.32532.0",
                    "Microsoft Visual C++ 2015-2022 Redistributable x86": "14.36.32532.0",
                    "Notepad++": "7.8.2",
                    "Meinberg": "4.2.4p6",
                    "Moxa": "3.0",
                    "Screen presser": "4.0"
                    }
                for software, version in search_name.items():  # Iterate through the dictionary
                    results = query_remote_registry(computer, registry_path_one, software)
                    if results == "[WinError 53] The network path was not found":
                        log_message = f"[WinError 53] The network path was not found for {computer}"
                        log_error(log_message)  
                    elif results:
                        for result in results:
                            software_version = result.get('DisplayVersion')
                            software_name = result.get('DisplayName')
                            if software_name == software and software_version == version:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                log_error(log_message)
                                helper += 1
                            else:
                                print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                log_error(log_message)                                                               
                    elif results:
                        # If no result from the first path, query the second registry path
                        results = query_remote_registry(computer, registry_path_two, software)
                        if results:
                            for result in results:
                                software_version = result.get('DisplayVersion')
                                if software_version == version:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"SUCCESS: {result['DisplayName']} Version {software_version} installed on {computer}"
                                    log_error(log_message)
                                    helper += 1
                                else:
                                    print(f"DisplayName: {result['DisplayName']}, DisplayVersion: {software_version}")
                                    log_message = f"ERROR: {result['DisplayName']} Installed with Version {software_version} instead of {version} on {computer}"
                                    log_error(log_message)          
                    else:
                            print(f"DisplayName: {software}, DisplayVersion: {version}")
                            log_message = f"ERROR: {software} {version} not Installed on {computer}"
                            log_error(log_message)
                if helper == softwares_numbers:
                    compare_main_result += 1
                    messagebox.showWARNING('Softwares', f"{computer} have all of the softwares installed" )
                    log_message = f"SUCCESS: {computer} have all of the softwares installed"
                    log_error(log_message) 
                else:
                    messagebox.showerror('Softwares', f"{computer} have {helper} of {softwares_numbers} softwares installed" )
                    log_message = f"ERROR: {computer} have {helper} of {softwares_numbers} softwares installed"
                    log_error(log_message)                                     

            if main_result == compare_main_result:
                b10.configure(bootstyle='SUCCESS')
                pbs.stop()
                pbs.place_forget
                pbs_label.place_forget
            else:
                b10.configure(bootstyle='DANGER')
                pbs.stop()
                pbs.place_forget()
                pbs_label.place_forget()
                
        # Start the threading
        threading.Thread(target=software_thread, daemon=True).start()

def system_check_health_all_system():
    # Update the main label with flexible positioning
    main_label.config(text='System Health', font=("Helvetica", 20))  # Change the main label
    main_label.place(relx=0.33, rely=0.15)  # 30% from left, 13% from top

    # Create WARNING label with flexible positioning
    WARNING_label = ttkb.Label(text='All System', font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    WARNING_label.place(relx=0.42, rely=0.22)  # 42% from left, 22% from top

    # Update the section label with flexible positioning
    section_label.config(text='system_check_health')  # Change the section label
    section_label.place(relx=0.36, rely=0.02)  # 38% from left, 2% from top

  # Adjusted to relative position

    # Hide the previous buttons
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b6.place_forget()

    # Create the Back button with relative positioning
    b7 = ttk.Button(root, text="Back", bootstyle=('WARNING', INSIDE), command=lambda: back(b9, b10, b11, b12, b7, cb2, cb1, sets_label, battey_label, projects_label, cb3, WARNING_label, entry_label, entry_value))
    b7.place(relx=0.02, rely=0.92)  # Positioned at 2% from left, 86% from top

    # Combobox for battery number selection
    def on_combobox_select(event):
        selected_value = cb1.get()
        if selected_value == "Enter Network":
            # Show the Entry widget for manual input
            entry_label.place(relx=0.65, rely=0.31)  # Positioned with relx/rely
            entry_value.place(relx=0.65, rely=0.35)
        else:
            # Hide the Entry widget if a number is selected
            entry_label.place_forget()
            entry_value.place_forget()

    # Battery label and combobox
    battey_label = ttkb.Label(text='Select Battery Number:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    battey_label.place(relx=0.36, rely=0.3)  # Positioned at 34% from left, 30% from top

    battnumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Enter Network"]
    cb1 = ttkb.Combobox(root, bootstyle='WARNING', values=battnumber)
    cb1.place(relx=0.36, rely=0.35)  # Positioned at 34% from left, 35% from top
    cb1.current(0)
    cb1.bind("<<ComboboxSelected>>", on_combobox_select)

    # Entry fields for network input
    entry_label = ttkb.Label(root, text="Enter Network:", font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    entry_value = ttkb.Entry(root, background="#000000")

    # Projects combobox
    projects = ['Spyder', 'All-in-One']
    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    projects_label.place(relx=0.36, rely=0.4)  # Positioned at 34% from left, 44% from top

    cb3 = ttkb.Combobox(root, bootstyle='WARNING', values=projects)
    cb3.place(relx=0.36, rely=0.45)  # Positioned at 34% from left, 49% from top
    cb3.current(0)

    # Sets combobox
    sets_label = ttkb.Label(text='Select Set:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    sets_label.place(relx=0.36, rely=0.5)  # Positioned at 34% from left, 54% from top

    if cb3.get() == 'All-in-One':
        sets = ['Main']
    else:
        sets = ['Main', 'Backup', 'Main+Backup']

    cb2 = ttkb.Combobox(root, bootstyle='WARNING', values=sets)
    cb2.place(relx=0.36, rely=0.55)  # Positioned at 34% from left, 59% from top
    cb2.current(0)

    # Action buttons
    b9 = ttk.Button(root, text="Networking", bootstyle=('WARNING', INSIDE), command=lambda: networking(cb1.get(), cb3.get(), cb2.get(), b9, diff_network=entry_value.get()), width=30)
    b9.place(relx=0.31, rely=0.71)  # Positioned at 31% from left, 71% from top

    b10 = ttk.Button(root, text="Softwares", bootstyle=('WARNING', INSIDE), command=lambda: software_check(cb1.get(), cb3.get(), cb2.get(), b10), width=30)
    b10.place(relx=0.31, rely=0.78)  # Positioned at 31% from left, 76% from top

    b11 = ttk.Button(root, text="Permissions", bootstyle=('WARNING', INSIDE), command=networking, width=30)
    b11.place(relx=0.31, rely=0.85)  # Positioned at 31% from left, 81% from top

    b12 = ttk.Button(root, text="Disk Space", bootstyle=('WARNING', INSIDE), command=networking, width=30)
    b12.place(relx=0.31, rely=0.92)  # Positioned at 31% from left, 86% from top

    
def system_check_health_self():
    main_label.config(text='System Health')   # Change the main label
    main_label.place(x=170,y=80)

    WARNING_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    WARNING_label.place(x=330,y=140)

    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(WARNING, INSIDE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,sets_label,battey_label,projects_label,cb3,WARNING_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(WARNING, INSIDE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='WARNING', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    sets_label = ttkb.Label(text='Select Component', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    sets_label.place(x=240,y=350)

    sets = ['CCU1','CCU2',"ICS1","ICS2","DRS1","DRS2","OC1","OC2","COP"]

    cb2 = ttkb.Combobox(root, bootstyle='WARNING', values=sets)
    cb2.place(x=240, y=380)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    projects_label.place(x=240,y=270)

    cb3 = ttkb.Combobox(root, bootstyle='WARNING', values=projects)
    cb3.place(x=240, y=300)
    cb3.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Networking", bootstyle=(WARNING, INSIDE), command=lambda:ping(cb1.get()))
    b9.place(x=240,y=450)

    b10 = ttk.Button(root, text="Softwares", bootstyle=(WARNING, INSIDE), command=networking)
    b10.place(x=370,y=450)

    b11 = ttk.Button(root, text="Permissions", bootstyle=(WARNING, INSIDE), command=networking)
    b11.place(x=240,y=495)

    b12 = ttk.Button(root, text="Disk Space", bootstyle=(WARNING, INSIDE), command=networking)
    b12.place(x=370,y=495)

def system_installation_Self():
    main_label.config(text='System Installation')   # Change the main label
    main_label.place(x=170,y=80)

    WARNING_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='WARNING')
    WARNING_label.place(x=330,y=140)

    section_label.config(text='system_Installation') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(WARNING, INSIDE), command=lambda:back2(b9,b10,b7,cb2,cb1,racks_label,battey_label,projects_label,cb3,WARNING_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(WARNING, INSIDE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='WARNING', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    racks_label = ttkb.Label(text='Select Component', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    racks_label.place(x=240,y=270)

    racks = ['CCU1','CCU2',"ICS1","ICS2","DRS1","DRS2","OC1","OC2","COP"]

    cb2 = ttkb.Combobox(root, bootstyle='WARNING', values=racks)
    cb2.place(x=240, y=300)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    projects_label.place(x=240,y=350)

    cb3 = ttkb.Combobox(root, bootstyle='WARNING', values=projects)
    cb3.place(x=240, y=380)
    cb3.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Spyder Software", bootstyle=(WARNING, INSIDE), command=networking)
    b9.place(x=200,y=450)

    b10 = ttk.Button(root, text="Third Party Softwares", bootstyle=(WARNING, INSIDE), command=networking)
    b10.place(x=370,y=450)

    # b11 = ttk.Button(root, text="Permissions", bootstyle=(WARNING, INSIDE), command=checker)
    # b11.place(x=240,y=495)

    # b12 = ttk.Button(root, text="Disk Space", bootstyle=(WARNING, INSIDE), command=checker)
    # b12.place(x=370,y=495)

def back2(b9, b10, b7, cb2, cb1, battey_label, sets_label, projects_label, cb3, WARNING_label):
    # Reset the main label and section label to default positions
    main_label.config(text='Spyder SU', font=("Helvetica", 52))
    main_label.place_configure(relx=0.26, rely=0.23) # Adjusting using relative positioning

    section_label.config(text='Main')
    section_label.place(relx=0.44, rely=0.02)  # Adjusting using relative positioning

    # Hide WARNING section and unnecessary widgets
    WARNING_label.place_forget()

    b9.place_forget()
    b10.place_forget()

    # Reset the main buttons' positions using relative positioning
    b1.place(relx=0.35, rely=0.47)  # Button 1
    b2.place(relx=0.35, rely=0.57)  # Button 2
    b3.place(relx=0.35, rely=0.67)  # Button 3
    b4.place(relx=0.35, rely=0.77)  # Button 4
    b6.place(relx=0.01, rely=0.85)  # Button 6

    # Hide unnecessary buttons
    b7.place_forget()

    # Hide combo boxes and labels that are not needed
    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    sets_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()


def back(b9, b10, b11, b12, b7, cb2, cb1, battey_label, sets_label, projects_label, cb3, WARNING_label, entry_label, entry_value):
    # Reset main label and section label to default positions
    main_label.config(text='Spyder SU', font=("Helvetica", 52))
    main_label.place(relx=0.21, rely=0.23)  # Relative positioning

    section_label.config(text='Main')
    section_label.place(relx=0.44, rely=0.02)  # Relative positioning

    # Hide the WARNING section and all buttons that are not needed
    WARNING_label.place_forget()

    b9.place_forget()
    b10.place_forget()
    b11.place_forget()
    b12.place_forget()

    # Reset the main buttons' positions using relative positioning
    b1.place(relx=0.33, rely=0.47)  # Button 1
    b2.place(relx=0.33, rely=0.57)  # Button 2
    b3.place(relx=0.33, rely=0.67)  # Button 3
    b4.place(relx=0.33, rely=0.77)  # Button 4
    b6.place(relx=0.01, rely=0.85)  # Button 6

    # Hide button 7 and other non-essential widgets
    b7.place_forget()

    # Hide combo boxes and labels that are not needed
    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    sets_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()

    # Hide entry labels and values
    entry_label.place_forget()
    entry_value.place_forget()

    # If you want the buttons to be flexible, adjust them dynamically
    # If you want fixed positioning, just keep using `place` as before
    # You can also add code to dynamically adjust button sizes based on the window size if necessary


# Create the main windows of the app
root = ttkb.Window(themename="cosmo")  # Set the root var value to the class tk
root.geometry('600x600')              # Set the size of the window
root.resizable(True, True)          # Set the option to resize the window to inactive
root.title('Spyder Software Update')  # Set the title of the app
root.iconbitmap("C:\Python Projects\Spyder-SU\Spyder-SU\images\spyder-bg.ico")
root.configure(background="#000000")

# Set a background image for the app
background_image = Image.open('C:\Python Projects\Spyder-SU\Spyder-SU\images\DAN.png')
image = ImageTk.PhotoImage(background_image)

image_label = ttk.Label(root, image=image, background="#000000")
image_label.place(relx=0.68, rely=0) # Adjusted to relative position

# Set Menu bars
app_menu = tk.Menu(root)
root.config(menu=app_menu)

# Create a menu item for "Open"
open_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Open', menu=open_menu)
open_menu.add_command(label='1. Softwares Installation Guid', command=networking)
open_menu.add_command(label='2. Softwares List', command=networking)

# Create a help menu item
help_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='1. mPrest integrators members', command=networking)
help_menu.add_command(label='2. About', command=networking)

# Create Labels
main_label = ttk.Label(text='Spyder SU', font=("Helvetica", 52), bootstyle='LIGHT', background="#000000")
main_label.place(relx=0.21, rely=0.23)  # Adjusted to relative position

section_label = ttk.Label(text='Main', bootstyle="WARNING", background="#000000",font=("Helvetica", 12))
section_label.place(relx=0.42, rely=0.02)  # Adjusted to relative position

local_ip = socket.gethostbyname(socket.gethostname())
hostname = socket.gethostname()
useraccount = os.getlogin()

runner_WARNING_label = ttk.Label(text=f'''
                               HOSTNAME: {hostname}
                               USER: {useraccount}
                               IP:{local_ip}''', background="#000000", bootstyle="WARNING")
runner_WARNING_label.place(relx=-0.15, rely=-0.012)  # Adjusted to relative position

# Create Buttons
b1 = ttk.Button(root, text="System Health Check (All System)", bootstyle=("WARNING", "INSIDE"), width=30, command=system_check_health_all_system)
b1.place(relx=0.33, rely=0.47)  # Adjusted to relative position

b2 = ttk.Button(root, text="System Health Check (Self)", bootstyle=("WARNING", "INSIDE"), width=30, command=system_check_health_self)
b2.place(relx=0.33, rely=0.57)  # Adjusted to relative position

b3 = ttk.Button(root, text="System Installation (All System)", bootstyle=("WARNING", "INSIDE"), width=30)
b3.place(relx=0.33, rely=0.67)  # Adjusted to relative position

b4 = ttk.Button(root, text="System Software Installation (Self)", bootstyle=("WARNING", "INSIDE"), width=30, command=system_installation_Self)
b4.place(relx=0.33, rely=0.77)  # Adjusted to relative position

#b5 = ttk.Button(root, text="ThirdParty Softwares Installation", bootstyle=(WARNING, INSIDE))
#b5.place(x=200,y=460)

b6 = ttk.Button(root, text="Exit", bootstyle=('WARNING', INSIDE), command=exit)
b6.place(relx=0.02, rely=0.92)

# Create Checkbutton
# var = IntVar()
# cb1 = ttkb.Checkbutton(bootstyle="danger, round-toggle", text="Ready!", variable=var, onvalue=1, offvalue=0, command=checker)
# cb1.place(x=300,y=300)



root.mainloop()                        #Allow the app to run without ending by itself
