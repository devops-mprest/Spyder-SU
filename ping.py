import subprocess
import datetime
import os
#from main import update_listboxes

current_working_dir = os.getcwd()

# Function to log errors to a file
def log_error(error_message):
    # Get the current time in a readable format
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Specify the log file path (adjust the path as needed)
    log_file = f"{current_working_dir}\Logs\\networking_logs.log"

    # Write the error message to the log file
    with open(log_file, 'a') as log:
        log.write(f"[{current_time}] {error_message}\n")

# The ping function
def ping(batt_number, project, set, update_treeview, permission_treeview, diff_network=None, cop_ip=None):
    components_ip = {}
    connected_devices = []
    disconnected_devices = []

    # Determine the IP addresses based on the settings
    if cop_ip:
        if diff_network and set == "Main":
            components_ip = {
                "MC2": f"{diff_network}.111",
                "MICS": f"{diff_network}.101",
                "MDB": f"{diff_network}.121",
                "OC1": f"{diff_network}.131",
                "COP": f"{cop_ip}"
            }
        elif diff_network and set == "Backup":
            components_ip = {
                "RC2": f"{diff_network}.112",
                "RICS": f"{diff_network}.102",
                "RDB": f"{diff_network}.122",
                "OC2": f"{diff_network}.132",
                "COP": f"{cop_ip}"
            }
        elif diff_network and set == "Main+Backup":
            components_ip = {
                "MC2": f"{diff_network}.111",
                "MICS": f"{diff_network}.101",
                "MDB": f"{diff_network}.121",
                "OC1": f"{diff_network}.131",
                "RC2": f"{diff_network}.112",
                "RICS": f"{diff_network}.102",
                "RDB": f"{diff_network}.122",
                "OC2": f"{diff_network}.132",
                "COP": f"{cop_ip}"
            }
        else:
            if project == "All-In-One":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "MICS": f"194.0.8{batt_number}.101",
                    "MDB": f"194.0.8{batt_number}.121",
                    "OC1": f"194.0.8{batt_number}.131",
                    "COP": f"{cop_ip}"
                }
            elif project == 'Spyder' and set == "Main":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "MICS": f"194.0.8{batt_number}.101",
                    "MDB": f"194.0.8{batt_number}.121",
                    "OC1": f"194.0.8{batt_number}.131",
                    "COP": f"{cop_ip}"
                }
            elif project == 'Spyder' and set == "Backup":
                components_ip = {
                    "RC2": f"194.0.8{batt_number}.112",
                    "RICS": f"194.0.8{batt_number}.102",
                    "RDB": f"194.0.8{batt_number}.122",
                    "OC2": f"194.0.8{batt_number}.132",
                    "COP": f"{cop_ip}"
                }
            elif project == 'Spyder' and set == "Main+Backup":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "RC2": f"194.0.8{batt_number}.112",
                    "MICS": f"194.0.8{batt_number}.101",
                    "RICS": f"194.0.8{batt_number}.102",
                    "MDB": f"194.0.8{batt_number}.121",
                    "RDB": f"194.0.8{batt_number}.122",
                    "OC1": f"194.0.8{batt_number}.131",
                    "OC2": f"194.0.8{batt_number}.132",
                    "COP": f"{cop_ip}"
                }
            else:
                return False  # If project doesn't match any known type
    
    # Case 2: When cop_ip is NOT provided
    else:
        if diff_network and set == "Main":
            components_ip = {
                "MC2": f"{diff_network}.111",
                "MICS": f"{diff_network}.101",
                "MDB": f"{diff_network}.121",
                "OC1": f"{diff_network}.131"
            }
        elif diff_network and set == "Backup":
            components_ip = {
                "RC2": f"{diff_network}.112",
                "RICS": f"{diff_network}.102",
                "RDB": f"{diff_network}.122",
                "OC2": f"{diff_network}.132"
            }
        elif diff_network and set == "Main+Backup":
            components_ip = {
                "MC2": f"{diff_network}.111",
                "MICS": f"{diff_network}.101",
                "MDB": f"{diff_network}.121",
                "OC1": f"{diff_network}.131",
                "RC2": f"{diff_network}.112",
                "RICS": f"{diff_network}.102",
                "RDB": f"{diff_network}.122",
                "OC2": f"{diff_network}.132"
            }
        else:
            if project == "All-In-One":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "MICS": f"194.0.8{batt_number}.101",
                    "MDB": f"194.0.8{batt_number}.121",
                    "OC1": f"194.0.8{batt_number}.131"
                }
            elif project == 'Spyder' and set == "Main":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "MICS": f"194.0.8{batt_number}.101",
                    "MDB": f"194.0.8{batt_number}.121",
                    "OC1": f"194.0.8{batt_number}.131"
                }
            elif project == 'Spyder' and set == "Backup":
                components_ip = {
                    "RC2": f"194.0.8{batt_number}.112",
                    "RICS": f"194.0.8{batt_number}.102",
                    "RDB": f"194.0.8{batt_number}.122",
                    "OC2": f"194.0.8{batt_number}.132"
                }
            elif project == 'Spyder' and set == "Main+Backup":
                components_ip = {
                    "MC2": f"194.0.8{batt_number}.111",
                    "RC2": f"194.0.8{batt_number}.112",
                    "MICS": f"194.0.8{batt_number}.101",
                    "RICS": f"194.0.8{batt_number}.102",
                    "MDB": f"194.0.8{batt_number}.121",
                    "RDB": f"194.0.8{batt_number}.122",
                    "OC1": f"194.0.8{batt_number}.131",
                    "OC2": f"194.0.8{batt_number}.132"
                }
            else:
                return False  # If project doesn't match any known type
    
    total_failure = 0
    connected_devices = []
    disconnected_devices = []

    # Ping each component
    for component, ip in components_ip.items():
        command = ["ping", "-n", "2", ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                connected_devices.append(component)
            else:
                disconnected_devices.append(component)
                total_failure += 1
        except Exception as e:
            total_failure += 1
            disconnected_devices.append(component)

        # Update the UI live after each ping
        update_treeview(permission_treeview, connected_devices, disconnected_devices)

    return total_failure, connected_devices, disconnected_devices