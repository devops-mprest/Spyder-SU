import subprocess
import platform
import threading

async def ping(batt_number):
    print(batt_number)
    command = ["ping", "-n", "3", f"8.8.{batt_number}.8"]
    try:
        # Run the ping command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check the return code
        if result.returncode == 0:
            print(f"Ping to 8.8.{batt_number}.8 successful!")
            print(result.stdout)
        else:
            print(f"Ping to 8.8.{batt_number}.8 failed!")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


