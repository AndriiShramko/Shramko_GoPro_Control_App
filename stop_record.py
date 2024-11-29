# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
import json
from concurrent.futures import ThreadPoolExecutor

def stop_recording(camera_ip):
    try:
        response = requests.get(f"http://{camera_ip}:8080/gopro/camera/shutter/stop")
        if response.status_code == 200:
            print(f"Recording stopped successfully on camera {camera_ip}.")
        else:
            print(f"Failed to stop recording on camera {camera_ip}. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while stopping recording on camera {camera_ip}: {e}")

if __name__ == "__main__":
    # Load devices from cache
    try:
        with open("camera_cache.json", "r") as cache_file:
            devices = json.load(cache_file)
        print("Loaded cached camera devices:")
        for device in devices:
            print(f"Name: {device['name']}, IP: {device['ip']}")
    except FileNotFoundError:
        print("Camera cache not found. Cannot stop recording.")
        exit()

    # Stop recording on all cameras
    print("Stopping recording on all cameras...")
    with ThreadPoolExecutor() as executor:
        executor.map(lambda d: stop_recording(d["ip"]), devices)
