# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
import json
from concurrent.futures import ThreadPoolExecutor
from goprolist_and_start_usb import discover_gopro_devices

def set_video_mode(camera_ip):
    try:
        response = requests.get(f"http://{camera_ip}:8080/gopro/camera/presets/load")
        if response.status_code == 200:
            print(f"Video mode set on camera {camera_ip}.")
        else:
            print(f"Failed to set video mode on camera {camera_ip}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while setting video mode on camera {camera_ip}: {e}")

def start_recording(camera_ip):
    try:
        response = requests.get(f"http://{camera_ip}:8080/gopro/camera/shutter/start")
        if response.status_code == 200:
            print(f"Recording started successfully on camera {camera_ip}.")
        else:
            print(f"Failed to start recording on camera {camera_ip}. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while starting recording on camera {camera_ip}: {e}")

if __name__ == "__main__":
    # Discover cameras
    devices = discover_gopro_devices()
    if devices:
        print("Found the following GoPro devices:")
        for device in devices:
            print(f"Name: {device['name']}, IP: {device['ip']}")

        # Save devices to cache
        with open("camera_cache.json", "w") as cache_file:
            json.dump(devices, cache_file)
        print("Camera devices cached successfully.")

        # Step 1: Prepare all cameras (video mode)
        for device in devices:
            set_video_mode(device["ip"])

        # Step 2: Start recording on all cameras simultaneously
        print("Starting recording on all cameras...")
        with ThreadPoolExecutor() as executor:
            executor.map(lambda d: start_recording(d["ip"]), devices)
    else:
        print("No GoPro devices found.")
