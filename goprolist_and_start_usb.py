# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

from zeroconf import Zeroconf, ServiceBrowser
import requests
import time
import logging
import socket
import json
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GoProListener:
    def __init__(self):
        self.devices = []

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            ip_address = ".".join(map(str, info.addresses[0]))
            logging.info(f"Discovered GoPro: {name} at {ip_address}")
            self.devices.append({
                "name": name,
                "ip": ip_address
            })

    def remove_service(self, zeroconf, service_type, name):
        logging.info(f"GoPro {name} removed")

# Discover GoPro devices
def discover_gopro_devices():
    zeroconf = Zeroconf()
    listener = GoProListener()
    logging.info("Searching for GoPro cameras...")
    browser = ServiceBrowser(zeroconf, "_gopro-web._tcp.local.", listener)

    try:
        time.sleep(5)  # Allow time for discovery
    finally:
        zeroconf.close()

    return listener.devices

def reset_and_enable_usb_control(camera_ip):
    logging.info(f"Resetting USB control on camera {camera_ip}.")
    toggle_usb_control(camera_ip, enable=False)
    time.sleep(2)
    toggle_usb_control(camera_ip, enable=True)

def toggle_usb_control(camera_ip, enable):
    action = 1 if enable else 0
    url = f"http://{camera_ip}:8080/gopro/camera/control/wired_usb?p={action}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"USB control {'enabled' if enable else 'disabled'} on camera {camera_ip}.")
        else:
            logging.error(f"Failed to {'enable' if enable else 'disable'} USB control on camera {camera_ip}. "
                          f"Status Code: {response.status_code}. Response: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Error toggling USB control on camera {camera_ip}: {e}")

if __name__ == "__main__":
    devices = discover_gopro_devices()
    if devices:
        logging.info("Found the following GoPro devices:")
        for device in devices:
            logging.info(f"Name: {device['name']}, IP: {device['ip']}")

        # Save discovered devices to cache
        with open("camera_cache.json", "w") as cache_file:
            json.dump(devices, cache_file, indent=4)
        logging.info("Cache updated successfully with newly discovered devices.")

        with ThreadPoolExecutor() as executor:
            executor.map(lambda d: reset_and_enable_usb_control(d['ip']), devices)
    else:
        logging.info("No GoPro devices found.")
