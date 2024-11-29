import logging
import subprocess
import sys
import os

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("goprolist_and_start_usb_sync_all_settings_date_time.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Function to execute a script with logging
def run_script(script_name):
    logging.info(f"Starting script: {script_name}")
    try:
        process = subprocess.Popen(
            [sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output = []
        for line in iter(process.stdout.readline, ""):
            logging.info(line.strip())
            output.append(line.strip())
        for line in iter(process.stderr.readline, ""):
            logging.error(line.strip())
            output.append(line.strip())
        process.stdout.close()
        process.stderr.close()
        process.wait()
        logging.info(f"Successfully completed script: {script_name}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running script {script_name}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logging.error(f"Script {script_name} not found. Make sure it is in the current directory.")
        sys.exit(1)

if __name__ == "__main__":
    configure_logging()

    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # List of scripts to execute in order
    scripts = [
        os.path.join(base_dir, "goprolist_and_start_usb.py"),
        os.path.join(base_dir, "read_and_write_all_settings_from_prime_to_other.py"),
        os.path.join(base_dir, "date_time_sync.py")
    ]

    total_cameras = 0

    # Run each script
    for script in scripts:
        output = run_script(script)
        if "read_and_write_all_settings_from_prime_to_other.py" in script:
            # Count cameras in the output
            camera_count = sum(1 for line in output if "Discovered GoPro:" in line and "at" in line)
            total_cameras = camera_count
            logging.info(f"Discovered {camera_count} cameras.")

    logging.info(f"All scripts executed successfully. Total cameras discovered: {total_cameras}.")

    # Run set_preset_0.py script after all others are completed
    set_preset_script = os.path.join(base_dir, "set_preset_0.py")
    run_script(set_preset_script)
    logging.info("Preset 0 set on all cameras.")
