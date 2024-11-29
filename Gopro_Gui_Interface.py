import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, messagebox
import subprocess
import threading
import time
import traceback
import os

class GoProControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GoPro Control Interface")
        self.is_recording = False
        self.log_content = []
        self.download_folder = None

        # Tabs
        self.tab_control = ttk.Notebook(root)

        self.control_tab = ttk.Frame(self.tab_control)
        self.download_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.control_tab, text="Control")
        self.tab_control.add(self.download_tab, text="Download & Format")
        self.tab_control.pack(expand=1, fill="both")

        # Control Tab
        self.connect_button = tk.Button(self.control_tab, text="Connect to Cameras", command=self.connect_to_cameras)
        self.connect_button.pack(pady=10)

        self.copy_settings_button = tk.Button(self.control_tab, text="Copy Settings from Prime Camera", command=self.copy_settings_from_prime_camera)
        self.copy_settings_button.pack(pady=10)

        self.record_button = tk.Button(self.control_tab, text="Record", command=self.toggle_record, bg="SystemButtonFace")
        self.record_button.pack(pady=10)

        self.turn_off_button = tk.Button(self.control_tab, text="Turn Off Cameras", command=self.turn_off_cameras)
        self.turn_off_button.pack(pady=10)

        # Log Window (Control Tab)
        self.log_frame = tk.Frame(self.control_tab)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, state="normal", height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Save Log Button
        self.save_log_button = tk.Button(self.control_tab, text="Save Log", command=self.save_log)
        self.save_log_button.pack(pady=5)

        # Show/Hide Log Button
        self.show_log_button = tk.Button(self.control_tab, text="Hide Log", command=self.toggle_log)
        self.show_log_button.pack(pady=5)

        self.log_visible = True

        # Download Tab
        self.download_label = tk.Label(self.download_tab, text="No folder selected", fg="blue")
        self.download_label.pack(pady=5)

        self.download_button = tk.Button(self.download_tab, text="Download all files from all Cameras", command=self.download_files)
        self.download_button.pack(pady=10)

        self.select_folder_button = tk.Button(self.download_tab, text="Select Download Folder", command=self.select_download_folder)
        self.select_folder_button.pack(pady=10)

        self.format_button = tk.Button(self.download_tab, text="Format All Cameras", command=self.format_all_cameras)
        self.format_button.pack(pady=10)

        # Log Window (Download Tab)
        self.download_log_frame = tk.Frame(self.download_tab)
        self.download_log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.download_log_text = scrolledtext.ScrolledText(self.download_log_frame, wrap=tk.WORD, state="normal", height=10)
        self.download_log_text.pack(fill=tk.BOTH, expand=True)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def log_message(self, message):
        self.log_content.append(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.yview(tk.END)
        self.download_log_text.insert(tk.END, f"{message}\n")
        self.download_log_text.yview(tk.END)

    def run_script(self, script_name, additional_args=None):
        try:
            script_path = os.path.join(self.base_dir, script_name)
            if not os.path.isfile(script_path):
                raise FileNotFoundError(f"Script {script_name} not found in {self.base_dir}")

            self.log_message(f"Running script: {script_path}")
            command = ["python", script_path]
            if additional_args:
                command.extend(additional_args)

            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
            )
            with process.stdout as stdout, process.stderr as stderr:
                for line in iter(stdout.readline, ""):
                    self.log_message(line.strip())
                for line in iter(stderr.readline, ""):
                    self.log_message(f"[ERROR] {line.strip()}")

            process.wait()
            if process.returncode == 0:
                self.log_message(f"Script {script_name} finished successfully.")
            else:
                self.log_message(f"Script {script_name} finished with errors. Exit code: {process.returncode}")
        except Exception as e:
            error_message = f"Error running {script_name}: {e}\n{traceback.format_exc()}"
            self.log_message(error_message)

    def connect_to_cameras(self):
        def countdown():
            countdown_time = 14
            while countdown_time > 0:
                self.connect_button.config(text=f"Connecting... ({countdown_time}s)")
                time.sleep(1)
                countdown_time -= 1
            self.connect_button.config(text="Connect to Cameras")

        def task():
            threading.Thread(target=countdown).start()
            output = self.run_script("goprolist_and_start_usb_sync_all_settings_date_time.py")
            camera_count = sum(1 for line in output if "Discovered GoPro:" in line and "at" in line)
            self.connect_button.config(text=f"Connected to {camera_count} cameras")

        threading.Thread(target=task).start()

    def copy_settings_from_prime_camera(self):
        threading.Thread(target=self.run_script, args=("read_and_write_all_settings_from_prime_to_other.py",)).start()

    def toggle_record(self):
        if not self.is_recording:
            threading.Thread(target=self.start_recording).start()
        else:
            threading.Thread(target=self.stop_recording).start()

    def start_recording(self):
        def countdown():
            countdown_time = 12
            while countdown_time > 0:
                self.record_button.config(text=f"Starting in {countdown_time}s", bg="yellow")
                time.sleep(1)
                countdown_time -= 1
            self.record_button.config(text="Stop", bg="red")

        threading.Thread(target=countdown).start()
        self.is_recording = True
        self.run_script("sync_and_record.py")
        start_time = time.time()
        while self.is_recording:
            elapsed = int(time.time() - start_time)
            self.record_button.config(text=f"Stop ({elapsed}s)")
            time.sleep(1)

    def stop_recording(self):
        self.is_recording = False
        self.run_script("stop_record.py")
        self.record_button.config(text="Record", bg="SystemButtonFace")

    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as log_file:
                log_file.write("\n".join(self.log_content))
            self.log_message(f"Log saved to {file_path}")

    def toggle_log(self):
        if self.log_visible:
            self.log_frame.pack_forget()
            self.show_log_button.config(text="Show Log")
        else:
            self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.show_log_button.config(text="Hide Log")
        self.log_visible = not self.log_visible

    def select_download_folder(self):
        self.download_folder = filedialog.askdirectory()
        if self.download_folder:
            self.download_label.config(text=f"Selected folder: {self.download_folder}", fg="green")
            self.log_message(f"Selected download folder: {self.download_folder}")

    def download_files(self):
        if not self.download_folder:
            self.log_message("Please select a download folder first.")
            return
        self.run_script("copy_to_pc_and_scene_sorting.py", [self.download_folder])

    def format_all_cameras(self):
        if messagebox.askyesno("Format SD Cards", "Format all cameras? This action cannot be undone."):
            self.run_script("format_sd.py")
            self.log_message("All cameras formatted.")

    def turn_off_cameras(self):
        self.run_script("Turn_Off_Cameras.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoProControlApp(root)
    root.mainloop()
