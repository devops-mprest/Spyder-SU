# Import the modules from the modules.py file
from modules import *
from app_functions import *
from ping import *
import subprocess
import threading
from tkinter import messagebox
import socket
import sys
from softwares import *
import sys
import csv
import os
import datetime
import ctypes
import queue
import wmi
import pythoncom

# Functions for networking check and threading

def software_map(computer, installed, not_installed):
    # Create a new top-level window
    status_window = tk.Toplevel(root)
    status_window.title(f"{computer} Software Status")

    # Create a label for installed software
    installed_label = ttk.Label(status_window, text="Installed Software:", font=("Arial", 12, "bold"))
    installed_label.pack(pady=10)

    # Create a Treeview to display installed software
    global installed_treeview  # Declare as global to access in the update function
    installed_treeview = ttk.Treeview(status_window, columns=("Software Name", "Version"), show="headings", height=10)
    installed_treeview.heading("Software Name", text="Software Name")
    installed_treeview.heading("Version", text="Version")
    installed_treeview.column("Software Name", width=400)
    installed_treeview.column("Version", width=200)
    installed_treeview.pack(padx=10, pady=5)

    # Create a label for not installed software
    not_installed_label = ttk.Label(status_window, text="Not Installed Software:", font=("Arial", 12, "bold"))
    not_installed_label.pack(pady=10)

    # Create a Treeview to display not-installed software
    global not_installed_treeview  # Declare as global to access in the update function
    not_installed_treeview = ttk.Treeview(status_window, columns=("Software Name", "Version"), show="headings", height=10)
    not_installed_treeview.heading("Software Name", text="Software Name")
    not_installed_treeview.heading("Version", text="Version")
    not_installed_treeview.column("Software Name", width=400)
    not_installed_treeview.column("Version", width=200)
    not_installed_treeview.pack(padx=10, pady=5)

    # Insert initial software lists (empty or default)
    for software_info in installed:
        software_name = software_info.get("software")
        version = software_info.get("version")
        installed_treeview.insert("", tk.END, values=(software_name, version))

    for software_info in not_installed:
        software_name = software_info.get("software")
        version = software_info.get("version")
        not_installed_treeview.insert("", tk.END, values=(software_name, version))

def update_software_map_treeview(computer, installed_software, not_installed_software):
    # Update the installed software treeview
    installed_treeview.delete(*installed_treeview.get_children())  # Clear the treeview before inserting new values
    for software_info in installed_software:
        software_name = software_info.get("software")
        version = software_info.get("version")
        installed_treeview.insert("", tk.END, values=(software_name, version))

    # Update the not installed software treeview
    not_installed_treeview.delete(*not_installed_treeview.get_children())  # Clear the treeview before inserting new values
    for software_info in not_installed_software:
        software_name = software_info.get("software")
        version = software_info.get("version")
        not_installed_treeview.insert("", tk.END, values=(software_name, version))

# Function to check disk space for a remote computer using WMI
def disk_space(pc):
    try:
        # Initialize COM for this thread
        pythoncom.CoInitialize()
        
        # Set up WMI connection to the remote machine
        connection = wmi.WMI(computer=pc)
        
        # Query for logical disks (C:, D:, etc.)
        disk_info = []
        for disk in connection.Win32_LogicalDisk(DriveType=3):  # DriveType=3 refers to local disks
            drive = disk.DeviceID
            total_space = int(disk.Size) / (1024 ** 3)  # Convert bytes to GB
            free_space = int(disk.FreeSpace) / (1024 ** 3)  # Convert bytes to GB
            used_space = total_space - free_space
            disk_info.append((drive, total_space, free_space, used_space))
        return disk_info
    except Exception as e:
        print(f"Error checking disk space on {pc}: {e}")
        return None
    finally:
        # Ensure to uninitialize COM when done with the thread
        pythoncom.CoUninitialize()

# Function to update the Treeview with disk space information for each computer
def update_treeview_disk(treeview, pc, disk_info):
    if disk_info:
        for drive, total, free, used in disk_info:
            # Find the matching row for the computer and drive, and update the status
            updated = False
            for item in treeview.get_children():
                if treeview.item(item)["values"][0] == pc and treeview.item(item)["values"][1] == drive:
                    treeview.item(item, values=(pc, drive, f"{free:.2f} GB Free"))
                    updated = True
                    break
            if not updated:
                # If not found, insert a new row
                treeview.insert('', 'end', values=(pc, drive, f"{free:.2f} GB Free"))
    else:
        # If the remote computer is unreachable or there is an error, update the status as 'Error'
        for item in treeview.get_children():
            if treeview.item(item)["values"][0] == pc:
                treeview.item(item, values=(pc, "Error", "Unable to retrieve disk space"))
                break

# Function to run the disk space check and update the Treeview
def run_disk_space_check(treeview, pc):
    # Query the disk space for the computer
    disk_info = disk_space(pc)
    
    # Update the Treeview with the retrieved disk space information
    update_treeview_disk(treeview, pc, disk_info)

# Function to start the disk space check in a separate thread for each computer
def check_disk_space_for_pc(treeview, pc):
    threading.Thread(target=run_disk_space_check, args=(treeview, pc), daemon=True).start()

# Main function to create the Disk Space window
def disk_space_window(battnumber, project, set, b12, cop_id):
    # Create the Toplevel window
    disk_space_window = tk.Toplevel(root)
    disk_space_window.title("Disk Space Status for Remote PCs")
    disk_space_window.geometry("800x400")  # Size of the new window

    # Create the Treeview widget
    treeview = ttk.Treeview(disk_space_window, columns=("Computer", "Drive", "Free Space"), show="headings")
    treeview.heading("Computer", text="Computer")
    treeview.heading("Drive", text="Drive")
    treeview.heading("Free Space", text="Free Space")
    treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Define remote computers based on the input parameters
    if set == 'Main+Backup':
        if cop_id:
            remote_computers = [
                r'pc-bene', 
                r'MC2-0{}'.format(battnumber),
                r'RC2-0{}'.format(battnumber),
                r'MICS-0{}'.format(battnumber),
                r'RICS-0{}'.format(battnumber),
                r'MDB-0{}'.format(battnumber),
                r'RDB-0{}'.format(battnumber),
                r'OC1'.format(battnumber),
                r'OC2'.format(battnumber),
                r'COP'.format(cop_id)
            ]
        else:
            remote_computers = [
                r'pc-bene', 
                r'MC2-0{}'.format(battnumber),
                r'RC2-0{}'.format(battnumber),
                r'MICS-0{}'.format(battnumber),
                r'RICS-0{}'.format(battnumber),
                r'MDB-0{}'.format(battnumber),
                r'RDB-0{}'.format(battnumber),
                r'OC1'.format(battnumber),
                r'OC2'.format(battnumber)
            ]

    # Add initial rows to the Treeview for each computer (initially "Checking...")
    for pc in remote_computers:
        treeview.insert('', 'end', values=(pc, "Checking...", "Initializing"))

    # Start the disk space check for each remote computer in separate threads
    for pc in remote_computers:
        check_disk_space_for_pc(treeview, pc)

# Function to check permissions on remote computers
def check_permission_to_c(battnumber, project, set, b11, cop_id):
    # Create a new top-level window for showing results
    status_window = tk.Toplevel(root)
    status_window.title(f"Permission Check Status")

    # Create a label for the status
    status_label = ttk.Label(status_window, text="Permission Check Results:", font=("Arial", 12, "bold"))
    status_label.pack(pady=10)

    # Create a Treeview to display the permission check results
    permission_treeview = ttk.Treeview(status_window, columns=("Computer Name", "Permission Status", "Error Message"), show="headings", height=10)
    
    # Define the column headings
    permission_treeview.heading("Computer Name", text="Computer Name")
    permission_treeview.heading("Permission Status", text="Permission Status")
    permission_treeview.heading("Error Message", text="Error Message")

    # Adjust column widths
    permission_treeview.column("Computer Name", width=200)
    permission_treeview.column("Permission Status", width=150)
    permission_treeview.column("Error Message", width=300)
    
    close_button = ttk.Button(status_window, text="Close", command=status_window.destroy)
    close_button.pack(pady=20)
    # Pack the Treeview widget with some padding
    permission_treeview.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Prepare the remote computers list based on the set
    if set == 'Main+Backup':
        if cop_id:
            remote_computers = [r'\\pc-bene', r'\\MC2-0{}'.format(battnumber), r'\\RC2-0{}'.format(battnumber), r'\\MICS-0{}'.format(battnumber), r'\\RICS-0{}'.format(battnumber), r'\\MDB-0{}'.format(battnumber), r'\\RDB-0{}'.format(battnumber), r'\\OC1'.format(battnumber), r'\\OC2'.format(battnumber), r'\\COP'.format(cop_id)]
        else:
            remote_computers = [r'\\pc-bene', r'\\MC2-0{}'.format(battnumber), r'\\RC2-0{}'.format(battnumber), r'\\MICS-0{}'.format(battnumber), r'\\RICS-0{}'.format(battnumber), r'\\MDB-0{}'.format(battnumber), r'\\RDB-0{}'.format(battnumber), r'\\OC1'.format(battnumber), r'\\OC2'.format(battnumber)]
    elif set == 'Main':
        if cop_id:
            remote_computers = [r'\\pc-bene', r'\\MC2-0{}'.format(battnumber), r'\\MICS-0{}'.format(battnumber), r'\\MDB-0{}'.format(battnumber), r'\\OC1'.format(battnumber), r'\\COP'.format(cop_id)]
        else:
            remote_computers = [r'\\pc-bene', r'\\MC2-0{}'.format(battnumber), r'\\MICS-0{}'.format(battnumber), r'\\MDB-0{}'.format(battnumber), r'\\OC1'.format(battnumber)]
    elif set == 'Backup':
        if cop_id:
            remote_computers = [r'\\pc-bene', r'\\RC2-0{}'.format(battnumber), r'\\RICS-0{}'.format(battnumber), r'\\RDB-0{}'.format(battnumber), r'\\OC2'.format(battnumber), r'\\COP'.format(cop_id)]
        else:
            remote_computers = [r'\\pc-bene', r'\\RC2-0{}'.format(battnumber), r'\\RICS-0{}'.format(battnumber), r'\\RDB-0{}'.format(battnumber), r'\\OC2'.format(battnumber)]

    # Start the progress bar
    b11.configure(bootstyle='info')
    pbp = ttk.Progressbar(root, bootstyle='info', mode="indeterminate", length=100)
    pbp.start(10)
    pbp.place(relx=0.73, rely=0.86)
    pbp_label = ttk.Label(root, text="Permissions Check In Progress", background="#000000", foreground="#FFFFFF")
    pbp_label.place(relx=0.68, rely=0.82)
    pbp_label.configure(text="Permissions Check In Progress")

    def create_file_on_pc(remote_computers, pbp):
        # Flag to track whether all checks are successful
        all_successful = True
        
        # Loop through each remote computer and check permissions
        for computer in remote_computers:
            try:
                remote_path = f"{computer}\\C$"  # Administrative share to access C: drive
                permission_status = "Success"
                error_message = ""

                if os.path.exists(remote_path):
                    print(f"Access to {remote_path} is available.")
                
                    test_file_path = f"{remote_path}\\test_permission_check.txt"
                    try:
                        with open(test_file_path, 'w') as test_file:
                            test_file.write(f"Permission check successful on {computer} at {datetime.datetime.now()}")
                            print(f"File created successfully at {test_file_path}")
                    
                        # Clean up after test
                        os.remove(test_file_path)
                        print(f"Test file {test_file_path} deleted.")
                    
                    except PermissionError:
                        permission_status = "Permission Denied"
                        error_message = f"Permission denied to create a file on {remote_path}\\C:\\."
                        all_successful = False  # If any check fails, mark as not successful
                    except Exception as e:
                        permission_status = "Error"
                        error_message = f"Error creating file: {str(e)}"
                        all_successful = False  # If any check fails, mark as not successful
                else:
                    permission_status = "Access Denied"
                    error_message = f"Access to {remote_path} is denied or the path does not exist."
                    all_successful = False  # If access is denied, mark as not successful

                # Insert result into the Treeview
                permission_treeview.insert("", tk.END, values=(computer, permission_status, error_message))
                permission_treeview.update_idletasks()
        
            except PermissionError:
                permission_status = "Permission Denied"
                error_message = f"Permission denied to access {computer}\\C\\."
                permission_treeview.insert("", tk.END, values=(computer, permission_status, error_message))
                permission_treeview.update_idletasks()
                all_successful = False  # If permission denied, mark as not successful
        
            except Exception as e:
                permission_status = "Error"
                error_message = f"An error occurred: {str(e)}"
                permission_treeview.insert("", tk.END, values=(computer, permission_status, error_message))
                permission_treeview.update_idletasks()
                all_successful = False  # If error occurs, mark as not successful

        # Stop the progress bar once all checks are done
        pbp.stop()
        pbp.place_forget()
        pbp_label.place_forget()

        # Change the color of the b11 button based on the results
        if all_successful:
            b11.configure(bootstyle='success')  # Set to green (successful)
        else:
            b11.configure(bootstyle='danger')  # Set to red (failed)

    # Create a new thread to run the permission check function asynchronously
    threading.Thread(target=create_file_on_pc, args=(remote_computers, pbp), daemon=True).start()

def update_treeview(permission_treeview, connected, disconnected):
    # Clear current data in Treeview
    for row in permission_treeview.get_children():
        permission_treeview.delete(row)

    # Insert connected devices as child nodes under the "Ping Status"
    for device in connected:
        permission_treeview.insert("", "end", text=device, values=(device, "Connected", ""))

    # Insert disconnected devices as child nodes under the "Ping Status"
    for device in disconnected:
        permission_treeview.insert("", "end", text=device, values=(device, "Disconnected", "Error: No response"))

    # Force the window to update (even if it's in a separate thread)
    permission_treeview.update_idletasks()
# The networking function
def networking(battnumber, project, set, b9, diff_network, cop_ip):
    global pb_label
    global pb

    # Create the progress bar and label
    b9.configure(bootstyle='info')
    pb = ttk.Progressbar(root, bootstyle='info', mode="indeterminate", length=100)
    pb.place(relx=0.73, rely=0.72)
    pb.start(10)
    pb_label = ttk.Label(root, text="Networking Check In Progress", background="#000000", foreground="#FFFFFF")
    pb_label.place(relx=0.68, rely=0.68)
    pb_label.configure(text="Networking Check In Progress")

    # Create the status window for connected and disconnected devices
    status_window = tk.Toplevel(root)
    status_window.title("Ping Status")

    # Create a label for the status
    status_label = ttk.Label(status_window, text="Ping Test Status:", font=("Arial", 12, "bold"))
    status_label.pack(pady=10)

    # Create a Treeview to display the ping status (connected/disconnected)
    permission_treeview = ttk.Treeview(status_window, columns=("Device", "Status", "Error Message"), show="headings", height=10)

    # Define the column headings
    permission_treeview.heading("Device", text="Device Name")
    permission_treeview.heading("Status", text="Status")
    permission_treeview.heading("Error Message", text="Error Message")

    # Adjust column widths
    permission_treeview.column("Device", width=200)
    permission_treeview.column("Status", width=150)
    permission_treeview.column("Error Message", width=300)

    # Pack the Treeview widget with some padding
    permission_treeview.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Add a close button
    close_button = ttk.Button(status_window, text="Close", command=status_window.destroy)
    close_button.pack(pady=20)

    # Start the thread to perform the ping operation
    def ping_thread():
        result = ping(battnumber, project, set, update_treeview, permission_treeview, diff_network, cop_ip)
        failures, connected, disconnected = result

        # If there are no failures, show success
        if failures == 0:
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
            messagebox.showerror("Ping Failed", "There were failures in the ping test.", icon="error")

    # Start the ping thread
    threading.Thread(target=ping_thread, daemon=True).start()

def software_check(battnumber, project, set, b10, cop_id=None):
    global pbs_label
    global pbs

    def log_error(error_message):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file = f"{current_working_dir}\\Logs\\softwares_logs.log"
        with open(log_file, 'a') as log:
            log.write(f"[{current_time}] {error_message}\n")

    if set == 'Main+Backup':
        if cop_id:
            remote_computers = [
                r'\\pc-bene',
                r'\\MC2-0{}'.format(battnumber),
                r'\\RC2-0{}'.format(battnumber),
                r'\\MICS-0{}'.format(battnumber),
                r'\\RICS-0{}'.format(battnumber),
                r'\\MDB-0{}'.format(battnumber),
                r'\\RDB-0{}'.format(battnumber),
                r'\\OC1'.format(battnumber),
                r'\\OC2'.format(battnumber),
                r'\\COP'.format(cop_id)
            ]
        else:
            remote_computers = [
                r'\\pc-bene',
                f'\\MC2-0{battnumber}',
                f'\\RC2-0{battnumber}',
                f'\\MICS-0{battnumber}',
                f'\\RICS-0{battnumber}',
                f'\\MDB-0{battnumber}',
                f'\\RDB-0{battnumber}',
                r'\\OC1',
                r'\\OC2'
            ]
        
        b10.configure(bootstyle='info')
        pbs = ttk.Progressbar(root, bootstyle='info', mode="indeterminate", length=100)
        pbs.start(10)
        pbs.place(relx=0.73, rely=0.79)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000", foreground="#FFFFFF")
        pbs_label.place(relx=0.68, rely=0.75)
        pbs_label.configure(text="Softwares Check In Progress")

        treeview_window = tk.Toplevel(root)
        treeview_window.title("Software Check Progress")
        treeview_window.geometry("800x400")  # Adjust the size as needed

        treeview = ttk.Treeview(treeview_window, columns=("Computer", "Software", "Status"), show="headings")
        treeview.heading("Computer", text="Computer")
        treeview.heading("Software", text="Software")
        treeview.heading("Status", text="Status")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def check_csv_for_computer(computer):
            csv_file = f"{current_working_dir}\\Config\\SoftwaresListConfig\\software_list_{computer}.csv"
            if os.path.exists(csv_file):
                search_name = {}
                with open(csv_file, newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) == 2:
                            software, version = row
                            search_name[software] = version
                return search_name
            else:
                log_message = f"ERROR: {csv_file} not found. Skipping software check for {computer}."
                log_error(log_message)
                print(f"ERROR: {csv_file} not found. Skipping software check for {computer}.")
                return None

        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0

            for computer in remote_computers:
                search_name = check_csv_for_computer(computer)

                if search_name is None:
                    continue

                installed_software = []
                not_installed_software = []
                for software, version in search_name.items():
                    # Check the first registry path
                    results = query_remote_registry(computer, registry_path_one, software)
                    
                    if results == "[WinError 53] The network path was not found":
                        log_message = f"[WinError 53] The network path was not found for {computer}"
                        log_error(log_message)
                    elif results:
                        for result in results:
                            software_version = result.get('DisplayVersion')
                            software_name = result.get('DisplayName')
                            if software_name == software and software_version == version:
                                installed_software.append({"software": software_name, "version": software_version})
                                compare_main_result += 1  # Increment successful result count
                            else:
                                not_installed_software.append({"software": software_name, "version": software_version})
                    else:
                        # If no results found in the first path, check the second path
                        results = query_remote_registry(computer, registry_path_two, software)
                        if results:
                            for result in results:
                                software_version = result.get('DisplayVersion')
                                software_name = result.get('DisplayName')
                                if software_name == software and software_version == version:
                                    installed_software.append({"software": software_name, "version": software_version})
                                    compare_main_result += 1  # Increment successful result count
                                else:
                                    not_installed_software.append({"software": software_name, "version": software_version})
                        else:
                            not_installed_software.append({"software": software, "version": version})

            # Now, compare main result to check if all computers were processed
            if main_result == compare_main_result:
                b10.configure(bootstyle='SUCCESS')
                pbs.stop()
                pbs.place_forget()
                pbs_label.place_forget()
                print("All software checks completed successfully.")
            else:
                b10.configure(bootstyle='DANGER')
                pbs.stop()
                pbs.place_forget()
                pbs_label.place_forget()
                print(f"Some software checks failed. Completed checks: {compare_main_result}/{main_result}")

        # Start the threading
        threading.Thread(target=software_thread, daemon=True).start()

    elif set == 'Main':
        if cop_id:
            remote_computers = [r'\\pc-bene',r'\\MC2-0{}'.format(battnumber),r'\\MICS-0{}'.format(battnumber),r'\\MDB-0{}'.format(battnumber),r'\\OC1'.format(battnumber),r'\\COP'.format(cop_id)]
        else:
            remote_computers = [r'\\pc-bene',r'\\MC2-0{}'.format(battnumber),r'\\MICS-0{}'.format(battnumber),r'\\MDB-0{}'.format(battnumber),r'\\OC1'.format(battnumber)]
        b10.configure(bootstyle='info')
        pbs = ttk.Progressbar(root, bootstyle='info', mode="indeterminate", length=100)
        pbs.start(10)
        pbs.place(relx=0.73, rely=0.79)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000",foreground="#FFFFFF")
        pbs_label.place(relx=0.68, rely=0.75)
        pbs_label.configure(text="Softwares Check In Progress")
        
        def check_csv(computer_file):
            csv_file = f"{current_working_dir}\Config\SoftwaresListConfig\software_list_{computer_file}.csv"
                # If the file exists, load it
            if os.path.exists(csv_file):
                search_name = {}
                with open(csv_file, newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) == 2:  # Ensure the row has software and version
                            software, version = row
                            search_name[software] = version
                return search_name
            else:
                print(f"{csv_file} not found. Using default software list.")
                return False  # Return default if file not found

        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0

            # Query the remote registry                 
            for computer in remote_computers:
                helper = 0
                if computer == "\\\\pc-bene":
                    if check_csv('pc-bene') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('pc-bene'))
                        search_name = check_csv('pc-bene')
                if computer == '\\\\MC2-0{}'.format(battnumber):
                    if check_csv('C2') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('C2'))
                        search_name = check_csv('C2')
                if computer == '\\\\MICS-0{}'.format(battnumber):
                    if check_csv('ICS') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('ICS'))
                        search_name = check_csv('ICS')
                if computer == '\\\\MDB-0{}'.format(battnumber):
                    if check_csv('DB') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('DB'))
                        search_name = check_csv('DB')
                if computer == '\\\\OC1-0{}'.format(battnumber):
                    if check_csv('OC') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('OC'))
                        search_name = check_csv('OC')
                if computer == "\\\\COP{}".format(cop_id):
                    if check_csv('COP') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('COP'))
                        search_name = check_csv('COP')
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
        if cop_id:
            remote_computers = [r'\\lap-maors',r'\\RC2-0{}'.format(battnumber),r'\\RICS-0{}'.format(battnumber),r'\\RDB-0{}'.format(battnumber),r'\\OC2'.format(battnumber),r'\\COP'.format(cop_id)]
        else:
            remote_computers = [r'\\lap-maors',r'\\RC2-0{}'.format(battnumber),r'\\RICS-0{}'.format(battnumber),r'\\RDB-0{}'.format(battnumber),r'\\OC2'.format(battnumber)]
        b10.configure(bootstyle='info')
        pbs = ttk.Progressbar(root, bootstyle='info', mode="indeterminate", length=100)
        pbs.start(10)
        pbs.place(relx=0.73, rely=0.79)
        pbs_label = ttk.Label(root, text="Softwares Check In Progress", background="#000000",foreground="#FFFFFF")
        pbs_label.place(relx=0.68, rely=0.75)
        pbs_label.configure(text="Softwares Check In Progress")
        
        def check_csv(computer_file):
            csv_file = f"{current_working_dir}\Config\SoftwaresListConfig\software_list_{computer_file}.csv"
                # If the file exists, load it
            if os.path.exists(csv_file):
                search_name = {}
                with open(csv_file, newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) == 2:  # Ensure the row has software and version
                            software, version = row
                            search_name[software] = version
                return search_name
            else:
                print(f"{csv_file} not found. Using default software list.")
                return False  # Return default if file not found

        def software_thread():
            registry_path_one = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            registry_path_two = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            main_result = len(remote_computers)
            compare_main_result = 0

            # Query the remote registry                 
            for computer in remote_computers:
                helper = 0
                if computer == "\\\\lap-maors":
                    if check_csv('lap-maors') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('lap-maors'))
                        search_name = check_csv('lap-maors')
                if computer == '\\\\RC2-0{}'.format(battnumber):
                    if check_csv('C2') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('C2'))
                        search_name = check_csv('C2')
                if computer == '\\\\RICS-0{}'.format(battnumber):
                    if check_csv('ICS') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('ICS'))
                        search_name = check_csv('ICS')
                if computer == '\\\\RDB-0{}'.format(battnumber):
                    if check_csv('DB') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('DB'))
                        search_name = check_csv('DB')
                if computer == '\\\\OC2-0{}'.format(battnumber):
                    if check_csv('OC') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('OC'))
                        search_name = check_csv('OC')
                if computer == "\\\\COP{}".format(cop_id):
                    if check_csv('COP') == False:
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
                        softwares_numbers = len(search_name)
                    else:
                        softwares_numbers = len(check_csv('COP'))
                        search_name = check_csv('COP')
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
    secondary_label = ttkb.Label(text='All System', font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    secondary_label.place(relx=0.42, rely=0.22)  # 42% from left, 22% from top

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
    b7 = ttk.Button(root, text="Back", bootstyle=('WARNING', INSIDE), command=lambda: back(b9, b10, b11, b12, b7, cb2, cb1, sets_label, battey_label, projects_label, cb3, secondary_label, entry_label, entry_value,cb4,with_cop_label,entry_cop_id_label,entry_cop_ip_label,entry_cop_ip_value,entry_cop_id_value))
    b7.place(relx=0.02, rely=0.92)  # Positioned at 2% from left, 86% from top

    # Combobox for battery number selection
    def on_combobox_select(event):
        selected_value = cb1.get()
        if selected_value == "Other":
            # Show the Entry widget for manual input
            entry_label.place(relx=0.65, rely=0.3)  # Positioned with relx/rely
            entry_value.place(relx=0.65, rely=0.339)
            cb3.configure(state=DISABLED)
        else:
            # Hide the Entry widget if a number is selected
            entry_label.place_forget()
            entry_value.place_forget()
            cb3.configure(state=NORMAL)

    def on_combobox_select2(event):
        selected_value = cb4.get()
        if selected_value == "Yes":
            # Show the Entry widget for manual input
            entry_cop_ip_label.place(relx=0.65, rely=0.57)  # Positioned with relx/rely
            entry_cop_ip_value.place(relx=0.65, rely=0.61)
            entry_cop_id_label.place(relx=0.80, rely=0.57)  # Positioned with relx/rely
            entry_cop_id_value.place(relx=0.80, rely=0.61)
        else:
            # Hide the Entry widget if a number is selected
            entry_cop_ip_label.place_forget()
            entry_cop_ip_value.place_forget()
            entry_cop_id_label.place_forget()
            entry_cop_id_value.place_forget()    

    # Battery label and combobox
    battey_label = ttkb.Label(text='Select Battery Number:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    battey_label.place(relx=0.36, rely=0.3)  # Positioned at 34% from left, 30% from top

    battnumber = [1, 2, 3, 4, 5, "Other"]
    cb1 = ttkb.Combobox(root, bootstyle='WARNING', values=battnumber)
    cb1.place(relx=0.36, rely=0.34)  # Positioned at 34% from left, 35% from top
    cb1.current(0)
    cb1.bind("<<ComboboxSelected>>", on_combobox_select)

    # Entry fields for network input
    entry_label = ttkb.Label(root, text="Enter Network:", font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    entry_value = ttkb.Entry(root, background="#000000")

    # Entry fieds for cop selection input
    entry_cop_ip_label = ttkb.Label(root, text="COP IP:", font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    entry_cop_ip_value = ttkb.Entry(root, background="#000000", width=11)

    entry_cop_id_label = ttkb.Label(root, text="COP ID:", font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    entry_cop_id_value = ttkb.Entry(root, background="#000000", width=5)

    # Projects combobox
    projects = ['Spyder', 'All-in-One']
    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    projects_label.place(relx=0.36, rely=0.39)  # Positioned at 34% from left, 44% from top

    cb3 = ttkb.Combobox(root, bootstyle='WARNING', values=projects)
    cb3.place(relx=0.36, rely=0.43)  # Positioned at 34% from left, 49% from top
    cb3.current(0)

    # Sets combobox
    sets_label = ttkb.Label(text='Select Set:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    sets_label.place(relx=0.36, rely=0.48)  # Positioned at 34% from left, 54% from top

    if cb3.get() == 'All-in-One':
        sets = ['Main']
    else:
        sets = ['Main', 'Backup', 'Main+Backup']

    cb2 = ttkb.Combobox(root, bootstyle='WARNING', values=sets)
    cb2.place(relx=0.36, rely=0.52)  # Positioned at 34% from left, 59% from top
    cb2.current(0)

    with_cop_label = ttkb.Label(text='With COP:', font=("Helvetica", 11), bootstyle='WARNING', background="#000000")
    with_cop_label.place(relx=0.36, rely=0.57)
    
    with_cop_list = ['No','Yes']
    cb4 = ttkb.Combobox(root, bootstyle='WARNING', values=with_cop_list)
    cb4.place(relx=0.36, rely=0.61)
    cb4.current(0)
    cb4.bind("<<ComboboxSelected>>", on_combobox_select2)    
    # Action buttons
    # connected = []
    # disconnected = []
    # map_b = ttk.Button(root, text="NM", bootstyle=('DARK', INSIDE),width=2.5, command=lambda: network_map(connected, disconnected))
    # map_b.place(relx=0.23, rely=0.71)

    b9 = ttk.Button(root, text="Networking", bootstyle=('WARNING', INSIDE), command=lambda: networking(cb1.get(), cb3.get(), cb2.get(), b9, diff_network=entry_value.get(), cop_ip=entry_cop_ip_value.get()), width=30)
    b9.place(relx=0.31, rely=0.71)  # Positioned at 31% from left, 71% from top

    b10 = ttk.Button(root, text="Softwares", bootstyle=('WARNING', INSIDE), command=lambda: software_check(cb1.get(), cb3.get(), cb2.get(), b10, cop_id=entry_cop_id_value.get()), width=30)
    b10.place(relx=0.31, rely=0.78)  # Positioned at 31% from left, 76% from top

    b11 = ttk.Button(root, text="Permissions", bootstyle=('WARNING', INSIDE), command=lambda: check_permission_to_c(cb1.get(), cb3.get(), cb2.get(), b11, cop_id=entry_cop_id_value.get()), width=30)
    b11.place(relx=0.31, rely=0.85)  # Positioned at 31% from left, 81% from top

    b12 = ttk.Button(root, text="Disk Space", bootstyle=('WARNING', INSIDE), command=lambda: disk_space_window(cb1.get(), cb3.get(), cb2.get(), b12, cop_id=entry_cop_id_value.get()), width=30)
    b12.place(relx=0.31, rely=0.92)  # Positioned at 31% from left, 86% from top
 
def system_check_health_self():
    main_label.config(text='System Health')   # Change the main label
    main_label.place(x=170,y=80)

    secondary_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='WARNING', background="#000000")
    secondary_label.place(x=330,y=140)

    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(WARNING, INSIDE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,sets_label,battey_label,projects_label,cb3,secondary_label))
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

    secondary_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='WARNING')
    secondary_label.place(x=330,y=140)

    section_label.config(text='system_Installation') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(WARNING, INSIDE), command=lambda:back2(b9,b10,b7,cb2,cb1,racks_label,battey_label,projects_label,cb3,secondary_label))
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

def back2(b9, b10, b7, cb2, cb1, battey_label, sets_label, projects_label, cb3, secondary_label):
    # Reset the main label and section label to default positions
    main_label.config(text='Spyder SU', font=("Helvetica", 52))
    main_label.place_configure(relx=0.26, rely=0.23) # Adjusting using relative positioning

    section_label.config(text='Main')
    section_label.place(relx=0.44, rely=0.02)  # Adjusting using relative positioning

    # Hide WARNING section and unnecessary widgets
    secondary_label.place_forget()

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

def back(b9, b10, b11, b12, b7, cb2, cb1, battey_label, sets_label, projects_label, cb3, secondary_label, entry_label, entry_value,cb4,with_cop_label,entry_cop_ip_label,entry_cop_id_label,entry_cop_ip_value,entry_cop_id_value):
    # Reset main label and section label to default positions
    main_label.config(text='Spyder SU', font=("Helvetica", 52))
    main_label.place(relx=0.21, rely=0.23)  # Relative positioning

    section_label.config(text='Main')
    section_label.place(relx=0.44, rely=0.02)  # Relative positioning

    # Hide the WARNING section and all buttons that are not needed
    secondary_label.place_forget()

    b9.place_forget()
    b10.place_forget()
    b11.place_forget()
    b12.place_forget()
    # map_b.place_forget()
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
    cb3.place_forget()
    projects_label.place_forget()
    cb4.place_forget()
    with_cop_label.place_forget()
    # Hide entry labels and values
    entry_label.place_forget()
    entry_value.place_forget()
    entry_cop_id_label.place_forget()
    entry_cop_ip_label.place_forget()
    entry_cop_ip_value.place_forget()
    entry_cop_id_value.place_forget()

    # If you want the buttons to be flexible, adjust them dynamically
    # If you want fixed positioning, just keep using `place` as before
    # You can also add code to dynamically adjust button sizes based on the window size if necessary



# Create the main windows of the app
current_working_dir = os.getcwd()
root = ttkb.Window(themename="cosmo")  # Set the root var value to the class tk
root.geometry('600x600')              # Set the size of the window
root.resizable(True, True)          # Set the option to resize the window to inactive
root.title('Spyder Software Update')  # Set the title of the app
root.iconbitmap(f'{current_working_dir}\images\spyder-bg.ico')
root.configure(background="#000000")

# Set a background image for the app
background_image = Image.open(f'{current_working_dir}\images\spyder-bg-back.jpeg')
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

runner_info_label = ttk.Label(text=f'''
                               HOSTNAME: {hostname}
                               USER: {useraccount}
                               IP:{local_ip}''', background="#000000", bootstyle="WARNING")
runner_info_label.place(relx=-0.15, rely=-0.012)  # Adjusted to relative position

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
