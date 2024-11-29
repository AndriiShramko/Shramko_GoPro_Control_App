# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import time
from date_time_sync import sync_time_on_cameras
from recording import discover_gopro_devices, set_video_mode, start_recording
from concurrent.futures import ThreadPoolExecutor

def sync_and_start_recording():
    # Step 1: Synchronize time on all cameras
    print("Starting time synchronization on all cameras...")
    sync_time_on_cameras()
    
    # Short pause after synchronization
    print("Waiting for 1 seconds before starting recording...")
    time.sleep(1)

    # Step 2: Discover cameras
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    print("Found the following GoPro devices:")
    for device in devices:
        print(f"Name: {device['name']}, IP: {device['ip']}")

    # Step 3: Set video mode
   # print("Setting video mode on all cameras...")
   # for device in devices:
   #     set_video_mode(device["ip"])

    # Step 4: Start recording
    print("Starting recording on all cameras...")
    with ThreadPoolExecutor() as executor:
        executor.map(lambda d: start_recording(d["ip"]), devices)

if __name__ == "__main__":
    sync_and_start_recording()
