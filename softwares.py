import subprocess

def run_wmi_query(computers):
    password = "Q1w2e3r4"  # Replace with your actual password

    for computer in computers:
        # Dynamically set the username to match the computer name
        username = f"{computer}\\Administrator"  # Assumes username is "Administrator" for each computer

        # Set the command as a PowerShell script with the dynamic username and computer name
        powershell_command = f"""
        $username = "{username}"
        $password = "{password}"
        $securePassword = ConvertTo-SecureString -String $password -AsPlainText -Force
        $credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)
        
        Get-WmiObject -Class Win32_Product -ComputerName {computer} -Credential $credential | Select-Object __SERVER, name, Version
        """
        
        try:
            # Run the PowerShell script using subprocess.run
            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
            )
            
            # Check the output
            print(f"WMI Query Results for {username} on {computer}:")
            print(result.stdout)
        
        except subprocess.CalledProcessError as e:
            print(f"Error executing the command for {username} on {computer}:")
            print(e.stderr)
        
        except Exception as e:
            print(f"An unexpected error occurred for {username} on {computer}: {str(e)}")


    # List of usernames to loop over
computers = ['MC2','RC2',"MICS","RICS","MDD","RDB","OC1","OC2"]

