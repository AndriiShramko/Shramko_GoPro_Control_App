import requests
from concurrent.futures import ThreadPoolExecutor
from goprolist_and_start_usb import discover_gopro_devices

def format_sd_card(camera):
    ip = camera["ip"]
    url = f"http://{ip}:8080/gp/gpControl/command/storage/delete/all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"SD card formatting successful on camera {ip}.")
        else:
            print(f"Failed to format SD card on camera {ip}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error connecting to camera {ip}: {e}")

def format_all_sd_cards():
    devices = discover_gopro_devices()
    if not devices:
        print("No GoPro devices found.")
        return

    print("Starting SD card formatting...")
    with ThreadPoolExecutor() as executor:
        executor.map(format_sd_card, devices)
    print("SD card formatting completed.")

if __name__ == "__main__":
    format_all_sd_cards()
