# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from goprolist_and_start_usb import discover_gopro_devices

# Function to synchronize time on all discovered cameras
def sync_time_on_cameras():
    # Discover connected cameras
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    # Get the list of IP addresses for all discovered cameras
    camera_ips = [device["ip"] for device in devices]

    # Get the current system time
    current_time = datetime.now()
    date = current_time.strftime("%Y_%m_%d")  # Format current date as YYYY_MM_DD
    time = current_time.strftime("%H_%M_%S")  # Format current time as HH_MM_SS
    timezone_offset = int(current_time.utcoffset().total_seconds() / 60) if current_time.utcoffset() else 0
    dst = 1 if current_time.dst() else 0

    # Function to synchronize time on a single camera
    def sync_camera_time(ip):
        url = f"http://{ip}:8080/gopro/camera/set_date_time"
        params = {
            "date": date,
            "time": time,
            "tzone": timezone_offset,
            "dst": dst
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print(f"Time synchronization successful on camera {ip}.")
            else:
                print(f"Failed to synchronize time on camera {ip}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to camera {ip}: {e}")

    # Synchronize time on all cameras concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(sync_camera_time, camera_ips)

if __name__ == "__main__":
    sync_time_on_cameras()
