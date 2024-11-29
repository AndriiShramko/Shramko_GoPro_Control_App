import sys
import os
import json
import logging
import requests
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor
from goprolist_and_start_usb import discover_gopro_devices

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_camera_status(camera_ip):
    logging.debug(f"Attempting to get status from camera at IP: {camera_ip}")
    try:
        response = requests.get(f"http://{camera_ip}:8080/gopro/camera/state", timeout=2)
        if response.status_code == 200:
            status = response.json()
            status_data = status.get("status", {})
            encoding_active = status_data.get("8")  # Assuming key "8" represents encoding status
            system_busy = status_data.get("31")  # Assuming key "31" represents system busy status
            recording_duration = status_data.get("13")  # Assuming key "13" represents recording time

            if system_busy:
                logging.debug(f"Camera {camera_ip} is currently busy.")
                return {"recording": False, "recording_duration": 0, "status": "Busy"}

            recording_status = "Recording" if encoding_active == 1 else "Not Recording"
            recording_duration = recording_duration if recording_duration is not None else 0
            logging.debug(f"Status for camera {camera_ip}: Recording: {encoding_active == 1}, Duration: {recording_duration} seconds")
            return {"recording": encoding_active == 1, "recording_duration": recording_duration}
        else:
            logging.error(f"Failed to get status from camera {camera_ip}. Status Code: {response.status_code}.")
            return {"error": "Failed to get status."}
    except requests.RequestException:
        logging.error(f"An error occurred while getting status from camera {camera_ip}: Connection timeout or unreachable.")
        return {"error": "Camera disconnected"}

class CameraUpdateThread(QThread):
    updated_devices_signal = pyqtSignal(list)

    def run(self):
        new_devices = discover_gopro_devices()
        self.updated_devices_signal.emit(new_devices)

class CameraStatusUpdateThread(QThread):
    updated_status_signal = pyqtSignal(dict)

    def __init__(self, devices):
        super().__init__()
        self.devices = devices

    def run(self):
        statuses = {}
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda d: get_camera_status(d), self.devices.keys()))

        for ip, status in zip(self.devices.keys(), results):
            statuses[ip] = status

        self.updated_status_signal.emit(statuses)

class CameraStatusGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        logging.debug("Initializing Camera Status GUI")
        self.setWindowTitle('GoPro Camera Status')
        self.setGeometry(100, 100, 600, 400)  # Set fixed size and position
        self.layout = QVBoxLayout()

        # Discover cameras
        logging.debug("Discovering GoPro devices...")
        self.devices = discover_gopro_devices()
        self.active_devices = {device['ip']: device for device in self.devices}
        
        self.total_connected_label = QLabel(f"Total cameras connected: {len(self.active_devices)}")
        self.layout.addWidget(self.total_connected_label)

        self.status_buttons = {}
        self.no_devices_label = QLabel("No GoPro devices found.")
        self.layout.addWidget(self.no_devices_label)

        if self.devices:
            logging.info(f"Found {len(self.devices)} GoPro devices.")
            self.no_devices_label.hide()
            for device in self.devices:
                serial_number = device['name'].replace("._gopro-web._tcp.local.", "")
                button = QPushButton(f"Camera: {serial_number}, IP: {device['ip']}, Status: Unknown, Duration: 0 seconds")
                self.status_buttons[device['ip']] = button
                self.layout.addWidget(button)

        # Add Record All and Stop All buttons with increased height and larger text
        self.record_all_button = QPushButton('Record All')
        self.record_all_button.setFixedHeight(150)  # Увеличиваем высоту кнопки в три раза
        self.record_all_button.setStyleSheet("font-size: 20px;")  # Увеличиваем размер шрифта пропорционально
        self.record_all_button.clicked.connect(self.record_all_cameras)
        self.layout.addWidget(self.record_all_button)

        self.stop_all_button = QPushButton('Stop All')
        self.stop_all_button.setFixedHeight(150)  # Увеличиваем высоту кнопки в три раза
        self.stop_all_button.setStyleSheet("font-size: 20px;")  # Увеличиваем размер шрифта пропорционально
        self.stop_all_button.clicked.connect(self.stop_all_cameras)
        self.layout.addWidget(self.stop_all_button)

        # Set up timer to refresh camera list every 5 seconds
        self.device_update_timer = QTimer(self)
        self.device_update_timer.timeout.connect(self.update_devices)
        self.device_update_timer.start(5000)

        # Set up timer to refresh camera status every 2.5 seconds
        self.status_update_timer = QTimer(self)
        self.status_update_timer.timeout.connect(self.update_status)
        self.status_update_timer.start(2500)

        self.setLayout(self.layout)

    def update_devices(self):
        if hasattr(self, 'device_update_thread') and self.device_update_thread.isRunning():
            return
        self.device_update_thread = CameraUpdateThread()
        self.device_update_thread.updated_devices_signal.connect(self.refresh_devices)
        self.device_update_thread.start()

    def refresh_devices(self, new_devices):
        logging.debug("Refreshing device list...")
        new_device_ips = {device['ip'] for device in new_devices}
        old_device_ips = set(self.active_devices.keys())

        # Handle newly added devices or reconnected devices
        for device in new_devices:
            if device['ip'] not in old_device_ips:
                logging.info(f"New camera detected: {device['name']} at {device['ip']}")
                self.active_devices[device['ip']] = device
                serial_number = device['name'].replace("._gopro-web._tcp.local.", "")
                
                if device['ip'] in self.status_buttons:
                    # Reconnect previously disconnected device
                    self.status_buttons[device['ip']].setText(f"Camera: {serial_number}, IP: {device['ip']}, Status: Unknown, Duration: 0 seconds")
                    self.status_buttons[device['ip']].setStyleSheet("background-color: none;")
                else:
                    # New device
                    button = QPushButton(f"Camera: {serial_number}, IP: {device['ip']}, Status: Unknown, Duration: 0 seconds")
                    self.status_buttons[device['ip']] = button
                    self.layout.addWidget(button)

        # Handle removed devices
        for ip in old_device_ips:
            if ip not in new_device_ips:
                logging.info(f"Camera disconnected: {self.active_devices[ip]['name']} at {ip}")
                self.status_buttons[ip].setText(f"Camera: {self.active_devices[ip]['name'].replace('._gopro-web._tcp.local.', '')}, IP: {ip}, Status: Disconnected")
                self.status_buttons[ip].setStyleSheet("background-color: gray;")

        # Refresh total connected cameras count
        self.total_connected_label.setText(f"Total cameras connected: {len(new_device_ips)}")

        # Remove 'No GoPro devices found.' label if cameras are found
        if new_devices:
            self.no_devices_label.hide()
        else:
            self.no_devices_label.show()

    def update_status(self):
        if hasattr(self, 'status_update_thread') and self.status_update_thread.isRunning():
            return
        self.status_update_thread = CameraStatusUpdateThread(self.active_devices)
        self.status_update_thread.updated_status_signal.connect(self.refresh_status)
        self.status_update_thread.start()

    def refresh_status(self, statuses):
        logging.debug("Refreshing status of all cameras...")
        for ip, status in statuses.items():
            if "error" in status:
                logging.error(f"Error getting status for camera {ip}: {status['error']}")
                self.status_buttons[ip].setText(f"Camera: {self.active_devices[ip]['name'].replace('._gopro-web._tcp.local.', '')}, IP: {ip}, Status: {status['error']}")
                self.status_buttons[ip].setStyleSheet("background-color: gray;")
            else:
                recording_status = "Busy" if status.get("status") == "Busy" else ("Recording" if status.get("recording", False) else "Not Recording")
                recording_duration = status.get("recording_duration", 0)
                self.status_buttons[ip].setText(f"Camera: {self.active_devices[ip]['name'].replace('._gopro-web._tcp.local.', '')}, IP: {ip}, Status: {recording_status}, Duration: {recording_duration} seconds")
                if status.get("recording", False):
                    self.status_buttons[ip].setStyleSheet("background-color: red;")
                else:
                    self.status_buttons[ip].setStyleSheet("background-color: none;")

    def run_script(self, script_name):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        if not os.path.isfile(script_path):
            logging.error(f"Script {script_name} not found at {script_path}")
            return

        logging.info(f"Running script: {script_path}")
        try:
            process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                logging.info(f"Script {script_name} finished successfully. Output: {stdout}")
            else:
                logging.error(f"Script {script_name} finished with errors. Exit code: {process.returncode}, Error: {stderr}")
        except Exception as e:
            logging.error(f"Error running script {script_name}: {e}")

    def record_all_cameras(self):
        logging.debug("Recording on all cameras...")
        self.run_script("goprolist_usb_activate_time_sync_record.py")

    def stop_all_cameras(self):
        logging.debug("Stopping recording on all cameras...")
        self.run_script("stop_record.py")

if __name__ == '__main__':
    logging.debug("Starting Camera Status Application")
    app = QApplication(sys.argv)
    gui = CameraStatusGUI()
    gui.show()
    sys.exit(app.exec_())
