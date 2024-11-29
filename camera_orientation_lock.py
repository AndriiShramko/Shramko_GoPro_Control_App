# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
from concurrent.futures import ThreadPoolExecutor
from goprolist_and_start_usb import discover_gopro_devices

# Function to set orientation on all discovered cameras
def set_orientation_on_cameras(orientation):
    """
    Set the orientation of all discovered GoPro cameras.

    Args:
        orientation (int): Orientation value (0, 1, 2, 3).
                          0 - upright, 1 - upside down, 2 - right side, 3 - left side.
    """
    # Discover connected cameras
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    # Get the list of IP addresses for all discovered cameras
    camera_ips = [device["ip"] for device in devices]

    # Function to set orientation on a single camera
    def set_camera_orientation(ip):
        url = f"http://{ip}:8080/gopro/camera/setting"
        params = {
            "setting": "86",  # Rotation setting ID
            "option": orientation  # Orientation value
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print(f"Orientation set to {orientation} on camera {ip}.")
            else:
                print(f"Failed to set orientation on camera {ip}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to camera {ip}: {e}")

    # Set orientation on all cameras concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(set_camera_orientation, camera_ips)

if __name__ == "__main__":
    desired_orientation = 0  # Set desired orientation (0, 1, 2, 3)
    set_orientation_on_cameras(desired_orientation)
