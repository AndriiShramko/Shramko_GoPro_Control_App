# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
from goprolist_and_start_usb import discover_gopro_devices
from concurrent.futures import ThreadPoolExecutor

def install_preset_on_all_cameras():
    # Discover GoPro devices
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    # Function to install preset on a single camera
    def install_preset(target_camera):
        target_ip = target_camera["ip"]
        preset_url = f"http://{target_ip}:8080/gopro/camera/presets/load?id=0"
        preset_response = requests.get(preset_url)

        if preset_response.status_code == 200:
            print(f"Preset successfully loaded on camera {target_ip}.")
        else:
            print(f"Failed to load preset on camera {target_ip}. Status Code: {preset_response.status_code}")

    # Install preset on all cameras concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(install_preset, devices)

if __name__ == "__main__":
    install_preset_on_all_cameras()
