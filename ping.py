import subprocess
import datetime
import os

# Function to log errors to a file
def log_error(error_message):
    # Get the current time in a readable format
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Specify the log file path (adjust the path as needed)
    log_file = "networking_logs.log"

    # Write the error message to the log file
    with open(log_file, 'a') as log:
        log.write(f"[{current_time}] {error_message}\n")

def ping(batt_number, project, set, update_progressbar,pb, diff_network=None):
    if diff_network and set == "Main":
        components_ip = {"MC2": f"{diff_network}.111",
                         "MICS": f"{diff_network}.101",
                         "MDB": f"{diff_network}.121",
                         "OC1": f"{diff_network}.131"}
    elif diff_network and set == "Backup":
        components_ip = {"RC2": f"{diff_network}.112",
                         "RICS": f"{diff_network}.102",
                         "RDB": f"{diff_network}.122",
                         "OC2": f"{diff_network}.132"}
    elif diff_network and set == "Main+Backup":
        components_ip = {"MC2": f"{diff_network}.111",
                         "MICS": f"{diff_network}.101",
                         "MDB": f"{diff_network}.121",
                         "OC1": f"{diff_network}.131",
                         "RC2": f"{diff_network}.112",
                         "RICS": f"{diff_network}.102",
                         "RDB": f"{diff_network}.122",
                         "OC2": f"{diff_network}.132"}      
    else:    
        if project == "All-In-One":
            components_ip = {"MC2": f"194.0.8{batt_number}.111",
                             "MICS": f"194.0.8{batt_number}.101",
                             "MDB": f"194.0.8{batt_number}.121",
                             "OC1": f"194.0.8{batt_number}.131"}
        elif project == 'Spyder' and set == "Main":
            components_ip = {"MC2": f"194.0.8{batt_number}.111",
                             "MICS": f"194.0.8{batt_number}.101",
                             "MDB": f"194.0.8{batt_number}.121",
                             "OC1": f"194.0.8{batt_number}.131"}
        elif project == 'Spyder' and set == "Backup":
            components_ip = {"RC2": f"194.0.8{batt_number}.112",
                             "RICS": f"194.0.8{batt_number}.102",
                             "RDB": f"194.0.8{batt_number}.122",
                             "OC2": f"194.0.8{batt_number}.132"}
        elif project == 'Spyder' and set =='Main+Backup':
            components_ip = {"MC2": f"194.0.8{batt_number}.111",
                             "RC2": f"194.0.8{batt_number}.112",
                             "MICS": f"194.0.8{batt_number}.101",
                             "RICS": f"194.0.8{batt_number}.102",
                             "MDB": f"194.0.8{batt_number}.121",
                            "RDB": f"194.0.8{batt_number}.122",
                            "OC1": f"194.0.8{batt_number}.131",
                            "OC2": f"194.0.8{batt_number}.132"}   
        else:
            return False
    
    total_failure = 0
    # progressbar_value = 0
    # Ping each component
    for component, ip in components_ip.items():
        command = ["ping", "-n", "2", ip]
        print(f"Pinging {component} {ip}...")
        try:
            # Run the ping command
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check the return code and print result for each component
            if result.returncode == 0:
                print(f"Ping to {ip} successful for {component}!")
                log_message = f"Ping succeeded for {component} ({ip}): {result.stderr}"
                log_error(log_message)
                # progressbar_value += 25
                # update_progressbar(pb, progressbar_value)
            else:
                print(f"Ping to {ip} failed for {component}!")
                error_message = f"Ping failed for {component} ({ip}): {result.stderr}"
                log_error(error_message)                
                print(result.stderr)
                total_failure += 1
                # progressbar_value += 25
                # update_progressbar(pb, progressbar_value)
        except Exception as e:
            print(f"An error occurred while pinging {component}: {e}")
            total_failure += 1
    return total_failure
