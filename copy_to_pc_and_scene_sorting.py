# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
from goprolist_and_start_usb import discover_gopro_devices
from prime_camera_sn import serial_number as prime_camera_sn  # Импортируем серийный номер основной камеры
from concurrent.futures import ThreadPoolExecutor

def create_folder_structure_and_copy_files(destination_root):
    print("Starting discovery of connected cameras...")
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return
    print(f"Discovered devices: {devices}")

    destination_root = Path(destination_root)
    destination_root.mkdir(parents=True, exist_ok=True)
    print(f"Destination root folder: {destination_root}")

    media_data = []

    def collect_media(camera):
        ip = camera["ip"]
        serial_number = camera["name"].split("._gopro-web._tcp.local.")[0]
        media_url = f"http://{ip}:8080/gopro/media/list"
        try:
            response = requests.get(media_url)
            if response.status_code == 200:
                media_list = response.json().get("media", [])
                for media in media_list:
                    for file in media.get("fs", []):
                        file_metadata = {
                            "serial_number": serial_number,
                            "ip": ip,
                            "folder": media.get("d"),
                            "name": file.get("n"),
                            "time": datetime.fromtimestamp(int(file.get("cre")))
                        }
                        media_data.append(file_metadata)
            else:
                print(f"Failed to get media list from camera {ip}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to camera {ip}: {e}")

    with ThreadPoolExecutor() as executor:
        executor.map(collect_media, devices)

    if not media_data:
        print("No media found on any camera.")
        return

    media_data.sort(key=lambda x: x["time"])
    scenes = []

    print("Sorting files into scenes...")
    for file in media_data:
        added_to_scene = False
        for scene in scenes:
            if abs((file["time"] - scene[0]["time"]).total_seconds()) <= 5:
                scene.append(file)
                added_to_scene = True
                break
        if not added_to_scene:
            scenes.append([file])

    print(f"Total scenes created: {len(scenes)}")

    total_files = 0
    for i, scene in enumerate(scenes, start=1):
        # Определение времени съемки с основной (прайм) камеры
        prime_file = next((f for f in scene if f["serial_number"] == prime_camera_sn), scene[0])
        timestamp = prime_file["time"].strftime("%Y_%m_%d_%H_%M_%S")
        
        # Создание названия папки с учетом времени съемки
        scene_folder_name = f"scene{i:02d}_{timestamp}"
        scene_folder = destination_root / scene_folder_name
        scene_folder.mkdir(parents=True, exist_ok=True)
        print(f"Scene {i}: {len(scene)} files")
        total_files += len(scene)

        for file in scene:
            source_url = f"http://{file['ip']}:8080/videos/DCIM/{file['folder']}/{file['name']}"
            destination_file = scene_folder / f"{file['serial_number']}_{file['name']}"
            print(f"Copying file {file['name']} from {file['ip']} to {destination_file}")
            try:
                with requests.get(source_url, stream=True) as response:
                    if response.status_code == 200:
                        with open(destination_file, "wb") as out_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                out_file.write(chunk)
                        print(f"File {file['name']} successfully copied.")
                    else:
                        print(f"Failed to download {file['name']} from {file['ip']}. Response code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error downloading {file['name']} from {file['ip']}: {e}")

    print(f"All files copied successfully: {total_files} files in {len(scenes)} scenes.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python copy_to_pc_and_scene_sorting.py <destination_root>")
        sys.exit(1)
    destination = sys.argv[1]
    create_folder_structure_and_copy_files(destination)
