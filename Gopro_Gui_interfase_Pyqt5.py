import sys
import os
import traceback
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ScriptRunner(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def __init__(self, script_path, additional_args=None):
        super().__init__()
        self.script_path = script_path
        self.additional_args = additional_args or []

    def run(self):
        try:
            if not os.path.isfile(self.script_path):
                raise FileNotFoundError(f"Script {self.script_path} not found.")

            self.output_signal.emit(f"Running script: {self.script_path}")
            command = ["python", self.script_path] + self.additional_args

            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
            )
            with process.stdout as stdout, process.stderr as stderr:
                for line in iter(stdout.readline, ""):
                    if line:
                        self.output_signal.emit(line.strip())
                for line in iter(stderr.readline, ""):
                    if line:
                        self.output_signal.emit(f"[ERROR] {line.strip()}")

            process.wait()
            if process.returncode == 0:
                self.output_signal.emit(f"Script {self.script_path} finished successfully.")
                self.finished_signal.emit(True)
            else:
                self.output_signal.emit(f"Script {self.script_path} finished with errors. Exit code: {process.returncode}")
                self.finished_signal.emit(False)

        except Exception as e:
            error_message = f"Error running {self.script_path}: {e}\n{traceback.format_exc()}"
            self.output_signal.emit(error_message)
            self.finished_signal.emit(False)


class GoProControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shramko Andrii GoPro Control Interface")
        self.is_recording = False
        self.log_content = []
        self.download_folder = None

        # Main Widget and Layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Tabs
        self.tab_control = QTabWidget()
        self.layout.addWidget(self.tab_control)

        self.control_tab = QWidget()
        self.download_tab = QWidget()

        self.tab_control.addTab(self.control_tab, "Control")
        self.tab_control.addTab(self.download_tab, "Download & Format")

        # Control Tab Layout
        self.control_layout = QVBoxLayout(self.control_tab)
        self.connect_button = QPushButton("Connect to Cameras")
        self.connect_button.clicked.connect(self.connect_to_cameras)
        self.control_layout.addWidget(self.connect_button)

        self.copy_settings_button = QPushButton("Copy Settings from Prime Camera")
        self.copy_settings_button.clicked.connect(self.copy_settings_from_prime_camera)
        self.control_layout.addWidget(self.copy_settings_button)

        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.toggle_record)
        self.control_layout.addWidget(self.record_button)

        self.set_preset_button = QPushButton("Set First Camera Preset on All Cameras")
        self.set_preset_button.clicked.connect(self.set_first_camera_preset)
        self.control_layout.addWidget(self.set_preset_button)

        self.turn_off_button = QPushButton("Turn Off Cameras")
        self.turn_off_button.clicked.connect(self.turn_off_cameras)
        self.control_layout.addWidget(self.turn_off_button)

        # Log Window (Control Tab)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.control_layout.addWidget(self.log_text)

        # Save Log Button
        self.save_log_button = QPushButton("Save Log")
        self.save_log_button.clicked.connect(self.save_log)
        self.control_layout.addWidget(self.save_log_button)

        # Download Tab Layout
        self.download_layout = QVBoxLayout(self.download_tab)

        self.download_label = QLabel("No folder selected")
        self.download_label.setStyleSheet("color: blue;")
        self.download_layout.addWidget(self.download_label)

        self.select_folder_button = QPushButton("Select Download Folder")
        self.select_folder_button.clicked.connect(self.select_download_folder)
        self.download_layout.addWidget(self.select_folder_button)

        self.download_button = QPushButton("Download all files from all Cameras")
        self.download_button.clicked.connect(self.download_files)
        self.download_layout.addWidget(self.download_button)

        self.format_button = QPushButton("Format All Cameras")
        self.format_button.clicked.connect(self.format_all_cameras)
        self.download_layout.addWidget(self.format_button)

        # Log Window (Download Tab)
        self.download_log_text = QTextEdit()
        self.download_log_text.setReadOnly(True)
        self.download_layout.addWidget(self.download_log_text)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def log_message(self, message):
        self.log_content.append(message)
        self.log_text.append(message)
        self.download_log_text.append(message)

    def run_script(self, script_name, button_to_enable, additional_args=None):
        script_path = os.path.join(self.base_dir, script_name)
        self.script_thread = ScriptRunner(script_path, additional_args)
        self.script_thread.output_signal.connect(self.log_message)
        self.script_thread.finished_signal.connect(lambda success: self.on_script_finished(success, button_to_enable))
        self.script_thread.start()

    def on_script_finished(self, success, button_to_enable):
        button_to_enable.setEnabled(True)
        if button_to_enable == self.record_button:
            if self.is_recording:
                self.record_button.setText("Stop")
            else:
                self.record_button.setText("Record")
        if not success:
            QMessageBox.critical(self, "Script Error", "The script did not complete successfully.")

    def connect_to_cameras(self):
        self.connect_button.setEnabled(False)
        self.connect_button.setText("Connecting...")
        self.run_script("goprolist_usb_activate_time_sync.py", self.connect_button)

    def copy_settings_from_prime_camera(self):
        self.copy_settings_button.setEnabled(False)
        self.run_script("read_and_write_all_settings_from_prime_to_other.py", self.copy_settings_button)

    def toggle_record(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.record_button.setEnabled(False)
        self.record_button.setText("Starting...")
        self.is_recording = True
        self.run_script("goprolist_usb_activate_time_sync_record.py", self.record_button)

    def stop_recording(self):
        self.record_button.setEnabled(False)
        self.is_recording = False
        self.run_script("stop_record.py", self.record_button)

    def set_first_camera_preset(self):
        self.set_preset_button.setEnabled(False)
        self.run_script("set_preset_0.py", self.set_preset_button)

    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as log_file:
                log_file.write("\n".join(self.log_content))
            self.log_message(f"Log saved to {file_path}")

    def select_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_folder = folder
            self.download_label.setText(f"Selected folder: {self.download_folder}")
            self.download_label.setStyleSheet("color: green;")
            self.log_message(f"Selected download folder: {self.download_folder}")

    def download_files(self):
        self.download_button.setEnabled(False)
        if not self.download_folder:
            self.log_message("Please select a download folder first.")
            self.download_button.setEnabled(True)
            return
        self.run_script("copy_to_pc_and_scene_sorting.py", self.download_button, [self.download_folder])

    def format_all_cameras(self):
        reply = QMessageBox.question(self, "Format SD Cards", "Format all cameras? This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.format_button.setEnabled(False)
            self.run_script("format_sd.py", self.format_button)

    def turn_off_cameras(self):
        self.turn_off_button.setEnabled(False)
        self.run_script("Turn_Off_Cameras.py", self.turn_off_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoProControlApp()
    window.show()
    sys.exit(app.exec_())
