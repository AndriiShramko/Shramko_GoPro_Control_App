# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
from goprolist_and_start_usb import discover_gopro_devices
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor

# Path to file containing the primary camera serial number
SERIAL_FILE = Path(__file__).parent / "prime_camera_sn.py"

# Function to read the primary camera serial number
def get_primary_camera_serial():
    try:
        with open(SERIAL_FILE, "r") as file:
            for line in file:
                if "serial_number" in line:
                    return line.split("=")[1].strip().strip("\"')")
    except Exception as e:
        print(f"Error reading primary camera serial file: {e}")
        return None

# Function to copy settings from the primary camera to others
def copy_camera_settings():
    # Get the list of discovered devices
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    # Get the primary camera serial number
    primary_serial = get_primary_camera_serial()
    if not primary_serial:
        print("Primary camera serial number not found.")
        return

    # Identify the primary camera and other cameras
    primary_camera = next((d for d in devices if primary_serial in d["name"]), None)
    if not primary_camera:
        print("Primary camera not found among discovered devices.")
        return

    target_cameras = [d for d in devices if d != primary_camera]

    if not target_cameras:
        print("No target cameras found for copying settings.")
        return

    # Get settings from the primary camera
    primary_ip = primary_camera["ip"]
    url = f"http://{primary_ip}:8080/gopro/camera/state"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to get settings from primary camera {primary_ip}. Status Code: {response.status_code}")
        return

    camera_state = response.json()
    settings = camera_state.get("settings", {})

    # Copy settings to all target cameras concurrently
    def copy_settings_to_camera(target_camera):
        target_ip = target_camera["ip"]
        for setting_id, value in settings.items():
            set_url = f"http://{target_ip}:8080/gopro/camera/setting"
            params = {
                "setting": setting_id,
                "option": value
            }
            set_response = requests.get(set_url, params=params)

            if set_response.status_code == 200:
                print(f"Setting {setting_id} successfully set to {value} on camera {target_ip}.")
            else:
                print(f"Failed to set setting {setting_id} to {value} on camera {target_ip}. Status Code: {set_response.status_code}")

    with ThreadPoolExecutor() as executor:
        # Copy settings to all target cameras
        print("Copying settings to all target cameras...")
        executor.map(copy_settings_to_camera, target_cameras)

if __name__ == "__main__":
    copy_camera_settings()
