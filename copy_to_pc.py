# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import os
import requests
from datetime import datetime
from pathlib import Path
from goprolist_and_start_usb import discover_gopro_devices
from concurrent.futures import ThreadPoolExecutor

def create_folder_structure_and_copy_files():
    # Discover connected cameras
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    # Get the current date for folder naming
    shoot_date = datetime.now().strftime("%Y-%m-%d")
    destination_root = Path.home() / "Documents" / "GoPro_Copies" / shoot_date
    destination_root.mkdir(parents=True, exist_ok=True)

    # Function to copy files from a single camera
    def copy_camera_files(camera):
        serial_number = camera["name"].split("._gopro-web._tcp.local.")[0]
        ip_address = camera["ip"]
        camera_dest_folder = destination_root / serial_number
        camera_dest_folder.mkdir(parents=True, exist_ok=True)

        # Get the list of media files on the camera
        media_url = f"http://{ip_address}:8080/gopro/media/list"
        try:
            response = requests.get(media_url)
            if response.status_code == 200:
                media_list = response.json().get("media", [])
                for media in media_list:
                    for file in media.get("fs", []):
                        file_name = file.get("n")
                        file_url = f"http://{ip_address}:8080/videos/DCIM/{media.get('d')}/{file_name}"
                        destination_file_name = f"{serial_number}_{file_name}"
                        destination_file_path = camera_dest_folder / destination_file_name

                        # Download and save the file
                        with requests.get(file_url, stream=True) as file_response:
                            if file_response.status_code == 200:
                                with open(destination_file_path, "wb") as out_file:
                                    for chunk in file_response.iter_content(chunk_size=8192):
                                        out_file.write(chunk)
                                print(f"File {file_name} copied to {destination_file_path}.")
                            else:
                                print(f"Failed to download {file_name} from {ip_address}.")
            else:
                print(f"Failed to get media list from camera {ip_address}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to camera {ip_address}: {e}")

    # Copy files concurrently from all cameras
    with ThreadPoolExecutor() as executor:
        executor.map(copy_camera_files, devices)

if __name__ == "__main__":
    create_folder_structure_and_copy_files()
