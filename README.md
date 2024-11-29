ECHO is on.
Here's a possible version of the text for users:

---

Please note: All the code and documentation were written by ChatGPT, so you might come across some of its "hallucinations." I did not meticulously check the documentation. I fed all my code into ChatGPT, and it wrote the docs by itself. I am sure that some parts are poorly written, but what matters is that the code works on my computer, and I can easily manage GoPro Hero 10 cameras synchronously in my scanner rig. As you go further, just keep in mind: ChatGPT-written docs aren't great, but they exist. :) 


# Shramko GoPro Control App

**Shramko GoPro Control App** is a powerful software solution designed for synchronizing and managing multiple GoPro Hero 10-11-12-13... cameras via USB. The application is capable of controlling up to 1000 cameras, allowing users to start/stop recording, adjust settings, synchronize time, and download files, all from a central interface.

This tool is perfect for projects that require multi-camera setups, such as **virtual studios**, **advertising shoots**, **music videos**, or **film productions**. With a focus on efficiency, it simplifies the management of large GoPro arrays, allowing studios and production teams to capture synchronized footage with ease.

## Key Features:
- **Full Camera Control**: Connect up to 100 GoPro Hero 10 cameras via USB.
- **Centralized Recording**: Start and stop recording on all cameras simultaneously.
- **Settings Management**: Adjust settings like ISO, shutter speed, and white balance on all cameras at once.
- **File Management**: Download files and automatically organize them into session-based folders for easy access.
- **Time Synchronization**: Ensure all cameras are perfectly synchronized for flawless multi-camera recordings.

## About the Author:
Developed by **Andrii Shramko**. For commercial licensing inquiries, please contact:
- **Email**: [zmei116@gmail.com](mailto:zmei116@gmail.com)
- **LinkedIn**: [Andrii Shramko](https://www.linkedin.com/in/andrii-shramko/)
## Project Structure:
- **Gopro_Gui_Interface.py**: Graphical user interface for controlling GoPro cameras.
- **Gopro_Gui_interfase_Pyqt5.py**: An advanced version of the GUI with additional features.
- **read_and_write_all_settings_from_prime_to_other.py**: Copies settings from the primary camera to all connected cameras.
- **recording.py**: Handles the start and stop of video recording.
- **sync_and_record.py**: Synchronizes time on all cameras before starting recording.
- **format_sd.py**: Formats SD cards on all connected GoPro cameras.
- **Turn_Off_Cameras.py**: Turns off all connected GoPro cameras.
## Installation

To install and run the Shramko GoPro Control App, follow these steps:

### Step 1: Clone the Repository
First, clone the repository to your local machine using Git:

```sh
git clone https://github.com/AndriiShramko/Shramko_GoPro_Control_App.git
cd Shramko_GoPro_Control_App

Step 2: Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. To set up a virtual environment, run the following commands:

sh
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:
sh
Copy code
venv\Scripts\activate
On MacOS/Linux:
sh
Copy code
source venv/bin/activate
Step 3: Install Dependencies
Once the virtual environment is activated, install all required dependencies listed in requirements.txt:

sh
Copy code
pip install -r requirements.txt
Step 4: Additional Requirements for GoPro Communication
Make sure you have the necessary USB drivers installed to communicate with GoPro cameras. You may need to follow specific setup instructions for enabling GoPro USB API communication.

Step 5: Run the Application
To start the application with a graphical user interface, run:

sh
Copy code
python Gopro_Gui_interfase_Pyqt5.py
or status_of_cameras_GUI.py
This will open the control interface, where you can manage multiple GoPro cameras simultaneously.

Copy code
Добавьте раздел "Требования":

Описание требований позволит пользователям понять, что им нужно для запуска проекта:
markdown
Copy code
## Requirements

- **Operating System**: Windows 10 or later
- **Python Version**: Python 3.11 or newer
- **Hardware**: USB connectivity for up to 100 GoPro Hero 10 cameras
- **Dependencies**: All dependencies are listed in `requirements.txt`. Make sure to install them using the steps in the Installation section.
Добавьте этот файл в git и закоммитьте:

## Requirements

- **Operating System**: Windows 10 or later
- **Python Version**: Python 3.11 or newer
- **Hardware**: USB connectivity for up to 1000 GoPro Hero 10-11-12-13 cameras
- **Dependencies**: All dependencies are listed in `requirements.txt`. Make sure to install them using the steps in the Installation section.

## How to Use the Application

Once the application is installed and all dependencies are set up, follow these steps to use the Shramko GoPro Control App:

### Step 1: Connect Your GoPro Cameras
- Connect up to 100 GoPro Hero 10 cameras to your computer via USB.
- Ensure all cameras are properly powered on and have compatible USB cables connected.

### Step 2: Launch the GUI
- Run the graphical user interface by executing:
  ```sh
  python Gopro_Gui_interfase_Pyqt5.py
The application interface will open, providing you with several control options for the connected cameras.
Step 3: Camera Control Options
Connect to Cameras: Use the "Connect to Cameras" button to establish a USB connection to all connected cameras.
Copy Settings from Prime Camera: After connecting, select "Copy Settings from Prime Camera" to apply settings from one camera to all others.
Record: Use the "Record" button to start/stop recording on all cameras simultaneously.
Set Camera Preset: Set a specific camera preset for all connected cameras.
Turn Off Cameras: Use the "Turn Off Cameras" button to safely power off all GoPro cameras.
Download Files: Go to the "Download & Format" tab to download all files from all cameras and organize them by session.
Format All Cameras: If needed, use the "Format All Cameras" button to clear all data from the SD cards in each camera.

## File Descriptions

Below is a detailed description of each file included in the project and its role.

### GUI Files
- **Gopro_Gui_Interface.py**: 
  - This file contains an initial version of the graphical user interface used for controlling GoPro cameras. It was designed to manage essential camera settings, such as connection and recording.
- **Gopro_Gui_interfase_Pyqt5.py**: 
  - An enhanced version of the GUI, built using PyQt5. It provides more advanced control options, such as managing multiple cameras, copying settings, and organizing files.
  - **Key Features**:
    - Graphical interface for intuitive control.
    - Tabs for different functionalities: "Control" for camera management and "Download & Format" for managing footage.
    - Real-time status updates and logs of operations.
- **status_of_cameras_GUI.py**:
  - This script provides a GUI for monitoring the status of all connected GoPro cameras. It displays whether cameras are recording, their current settings, and any errors that occur.
  - **Usage**:
    - View real-time statuses such as battery level, recording duration, and connection state.

### Supporting Files for GUI
- **camera_cache.json**:
  - This file is used to store cached data about the connected cameras. It helps speed up subsequent connections and saves some user-specific settings.
- **prime_camera_sn.py**:
  - Contains the serial number of the primary GoPro camera. This camera is used as a reference to copy settings to all other connected cameras.

## Camera Control and Supporting Scripts

The project includes several scripts designed to directly manage the connected GoPro cameras, synchronize settings, and ensure smooth operation during recording sessions.

### Camera Control Scripts
- **goprolist_and_start_usb.py**:
  - **Description**: This script is responsible for discovering all connected GoPro cameras and initializing USB connections. It scans available USB ports to identify connected GoPro devices and establishes the communication channel.
  - **Usage**: This script is typically run at the start to detect and prepare the cameras for further actions.

- **goprolist_usb_activate_time_sync.py**:
  - **Description**: Activates time synchronization on all discovered GoPro cameras. This script ensures that all connected cameras are synchronized to the same time, which is crucial for multi-camera recordings.
  - **Usage**: Run this script to set a common time reference for all cameras, reducing post-production issues with unsynchronized footage.

- **read_and_write_all_settings_from_prime_to_other.py**:
  - **Description**: Copies settings from a primary camera (the one defined in `prime_camera_sn.py`) to all other discovered cameras. This ensures that all cameras have identical settings for consistent recording.
  - **Usage**: This script is particularly useful for complex multi-camera setups where each camera needs identical parameters such as resolution, frame rate, ISO, and white balance.

- **recording.py**:
  - **Description**: Handles the start and stop of recording on all connected cameras. The script sends commands to all connected GoPros to begin or end recording, providing a synchronized start across multiple cameras.
  - **Usage**: This is a core script used during shooting, allowing the user to begin or end recording without manually operating each camera.

- **sync_and_record.py**:
  - **Description**: A combined script that first synchronizes the time on all cameras using `date_time_sync.py` and then starts recording. It ensures a seamless process for synchronization and capturing footage.
  - **Usage**: Ideal for users who need an integrated solution for synchronizing time and immediately starting the recording process.

- **set_preset_0.py**:
  - **Description**: Applies a predefined camera preset (preset 0) to all connected GoPros. Presets include specific settings such as resolution, field of view, and frame rate.
  - **Usage**: This script is helpful when needing to switch all cameras to a specific setup quickly.

### Supporting Scripts
- **date_time_sync.py**:
  - **Description**: Synchronizes the system date and time with all connected GoPro cameras. This is important for multi-camera environments to ensure all cameras are recording at the exact same moment.
  - **Usage**: This script is typically run before any recording session, especially when multiple cameras are used in a time-critical shoot.

- **prime_camera_sn.py**:
  - **Description**: Stores the serial number of the primary camera. This is used to identify which camera’s settings are to be copied to all other cameras in the setup.
  - **Usage**: You can modify this file to set a new primary camera for copying settings.

- **format_sd.py**:
  - **Description**: Formats the SD cards on all connected GoPro cameras. It’s a quick way to ensure all cameras have enough storage for a new session.
  - **Usage**: Use this script with caution, as it will delete all data on the SD cards.

- **Turn_Off_Cameras.py**:
  - **Description**: Turns off all connected GoPro cameras to save power when they are not in use.
  - **Usage**: Run this script at the end of the shooting session to turn off all cameras without manual intervention.
## File Management Scripts

These scripts are used to download, sort, and manage the footage recorded by the GoPro cameras. They simplify the process of collecting and organizing videos from multiple cameras, which is especially useful for large projects.

### Download and Sort Scripts
- **copy_to_pc.py**:
  - **Description**: Copies footage from all connected GoPro cameras to a specified folder on your computer. The script handles each camera individually and makes sure that all footage is safely downloaded.
  - **Usage**: Run this script to quickly transfer all recorded footage from the cameras to your computer. You will be prompted to select a target directory where the footage will be saved.

- **copy_to_pc_and_scene_sorting.py**:
  - **Description**: Extends the basic download functionality by also sorting the videos into session-based folders. Each folder represents a recording session, and the videos within are named according to the camera that captured them. This is useful for managing footage from multiple takes or scenes.
  - **Usage**: Use this script when you need an organized structure for your footage, making post-production more manageable. The script will create one folder per recording session and will place all videos (one from each camera) into that folder.

### File Handling and Utilities
- **status_of_cameras.py**:
  - **Description**: Retrieves and displays the current status of all connected cameras. This includes information such as recording state, battery level, and connection status.
  - **Usage**: Use this script to monitor the state of the cameras before, during, or after a recording session. It is useful for ensuring that all cameras are functioning properly.

- **status_of_cameras_GUI.py**:
  - **Description**: A GUI version of `status_of_cameras.py` that provides a graphical interface to easily view the status of all connected GoPro cameras. It displays information in real time, allowing users to quickly assess the status of the entire camera setup.
  - **Usage**: This script is recommended for users who prefer a visual representation of camera statuses. It is particularly helpful for identifying issues with specific cameras.

- **sleep.py**:
  - **Description**: A simple utility script used to pause the execution of other scripts. This is useful for creating delays between commands, such as waiting for all cameras to finish an operation before proceeding.
  - **Usage**: You may see this script used as a helper in other scripts to provide necessary delays for stable operation.

## Auxiliary Scripts and Utilities

The following scripts and utilities provide additional support to the core functionality of the Shramko GoPro Control App. These files help automate and streamline the workflow for managing multiple cameras and executing commands across them.

### Auxiliary Utility Scripts
- **set_video_mode.py**:
  - **Description**: Sets the video mode on all connected GoPro cameras. This script configures the video resolution, frame rate, and field of view settings based on predefined preferences.
  - **Usage**: Run this script to ensure that all cameras are set to the correct video mode before starting a recording session. This prevents inconsistencies across footage.

- **camera_orientation_lock.py**:
  - **Description**: Locks the orientation of all connected cameras to prevent unintended changes during recording. This script ensures that each camera maintains the correct orientation (e.g., landscape) throughout the session.
  - **Usage**: Use this script if you need to lock the cameras in a specific orientation, which is particularly useful for ensuring uniform video perspectives.

- **goprolist_and_start_usb_sync_all_settings_date_time.py**:
  - **Description**: This script combines multiple functionalities to provide a streamlined way of initializing the camera setup. It discovers connected GoPro cameras, synchronizes their time, and copies settings from the primary camera to others.
  - **Usage**: This is a useful script to run at the beginning of a shooting session to make sure all cameras are synced in terms of time and settings.

- **goprolist_and_start_usb_sync_all_settings_date_time copy.py**:
  - **Description**: This file is a modified version of the original `goprolist_and_start_usb_sync_all_settings_date_time.py`. It contains adjustments tailored for specific scenarios or configurations.
  - **Usage**: Use this file only if the original script requires custom modifications for unique setup requirements.

- **stop_record.py**:
  - **Description**: Stops recording on all connected GoPro cameras. This script ensures that all cameras cease recording simultaneously to avoid issues with unsynchronized footage.
  - **Usage**: Run this script after a recording session to ensure all cameras stop recording at the same time.

- **sleep.py**:
  - **Description**: Provides a delay between commands. This utility script is used internally to ensure there are appropriate pauses between operations when interacting with the cameras, which can prevent issues caused by sending commands too quickly.
  - **Usage**: Typically used as a helper script in combination with other commands.

### Miscellaneous Resources
- **icon.ico** and **ico/a2d48c62-b5d0-4da1-b944-ff767a22f643.jpg**:
  - **Description**: These files contain icons used for the graphical user interface (GUI). They provide branding and visual cues to enhance the user experience.
  - **Usage**: These icons are included when building the GUI application into an executable file to provide a professional appearance.

## Building the Project into an Executable File

The Shramko GoPro Control App can be built into a standalone executable (`.exe`) file using **PyInstaller**. This allows you to distribute the software without requiring users to install Python or any dependencies.

### Step-by-Step Instructions

Follow these steps to create an `.exe` file from the source code:

### Step 1: Install PyInstaller
- To begin, you need to install PyInstaller. Make sure you are in your virtual environment if you are using one:
  ```sh
  pip install pyinstaller
Step 2: Navigate to the Project Directory
Open a terminal or command prompt, and navigate to the root directory of the project:
sh
Copy code
cd path/to/Shramko_GoPro_Control_App
Step 3: Create the .exe File
Use PyInstaller to create a standalone .exe file for the main application script (Gopro_Gui_interfase_Pyqt5.py). Run the following command:
sh
Copy code
pyinstaller --onefile --icon=icon.ico --noconsole Gopro_Gui_interfase_Pyqt5.py
Options Explained:
--onefile: Combines everything into a single executable file.
--icon=icon.ico: Adds an icon to the executable, making it more visually appealing.
--noconsole: Suppresses the console window when running the GUI application.
Step 4: Locate the Executable
Once the process is complete, the .exe file will be located in the dist folder within your project directory. The resulting executable file will be named Gopro_Gui_interfase_Pyqt5.exe.
Step 5: Create a Portable Version
If you need a portable version (so users do not have to install it), simply distribute the .exe file along with any necessary resource files (e.g., icons, configuration files). Place all files in one folder and ensure they remain together during use.
Step 6: Additional Notes
Icon and Branding: You can change the icon by replacing icon.ico with your own .ico file.
Dependency Management: PyInstaller will automatically include all Python dependencies, but you may need to manually add additional files that are required by your scripts (e.g., camera_cache.json or any other resources).
Testing: After creating the .exe, it is recommended to test it on a different computer (preferably without Python installed) to ensure all dependencies are correctly bundled.
Example Command for status_of_cameras_GUI.py
To create an executable for the status_of_cameras_GUI.py script, use the following command:
sh
Copy code
pyinstaller --onefile --icon=icon.ico --noconsole status_of_cameras_GUI.py
Copy code
## FAQ and Troubleshooting

This section addresses common issues users may encounter and provides solutions to help troubleshoot problems during installation, setup, and use of the Shramko GoPro Control App.

### Frequently Asked Questions

#### 1. **I connected multiple GoPro cameras, but the app does not detect them. What should I do?**
- **Solution**: 
  - Ensure that all cameras are properly powered on and connected via USB. Verify that each USB port is functioning.
  - Run the script `goprolist_and_start_usb.py` to manually discover the cameras.
  - Check the USB drivers on your computer to confirm they support GoPro devices. Reinstall the drivers if necessary.

#### 2. **Why am I getting a "ModuleNotFoundError" when I try to run the `.exe` file?**
- **Solution**: 
  - This usually occurs because some Python modules were not included during the build. Ensure that you use the `--hidden-import` option with PyInstaller to explicitly include any missing modules.
  - For example, if you receive an error related to `zeroconf`, run PyInstaller with additional hidden imports:
    ```sh
    pyinstaller --onefile --icon=icon.ico --noconsole --hidden-import=zeroconf Gopro_Gui_interfase_Pyqt5.py
    ```

#### 3. **How do I reset the settings of all GoPro cameras to default?**
- **Solution**: 
  - Use the script `read_and_write_all_settings_from_prime_to_other.py` to overwrite settings across all cameras. Set up a primary camera with the desired default settings, then run the script to copy these settings to all others.

#### 4. **I am experiencing delays when starting/stopping recording. Is this normal?**
- **Solution**: 
  - Delays in starting or stopping recording across multiple cameras are normal due to the time it takes to send USB commands to each camera. You can reduce potential latency by ensuring that no other USB devices are occupying bandwidth.
  - Additionally, ensure that all cables are functioning properly and that there are no connection issues.

#### 5. **Why do I see warnings like "LF will be replaced by CRLF" during `git add`?**
- **Solution**: 
  - This is a line-ending warning. It means that Git is converting line endings from Unix style (LF) to Windows style (CRLF). You can avoid these warnings by setting your line endings preference in Git configuration:
    ```sh
    git config --global core.autocrlf true
    ```
  - This setting will automatically convert line endings based on the operating system.

#### 6. **How can I update the firmware of my GoPro cameras using this tool?**
- **Solution**: 
  - Currently, the application does not support direct firmware updates for GoPro cameras. You must manually update the firmware following GoPro's official guidelines.

### Troubleshooting Common Issues

#### Problem: **USB Connection Issues**
- **Solution**:
  - Make sure all cameras are using compatible USB cables.
  - Disconnect and reconnect the cameras, ensuring the computer recognizes each device.
  - Run `goprolist_and_start_usb.py` to reinitialize the connection if needed.

#### Problem: **PyInstaller Missing Modules During `.exe` Build**
- **Solution**:
  - If PyInstaller is missing modules during the build process, explicitly add those modules using the `--hidden-import` argument. For example:
    ```sh
    pyinstaller --onefile --hidden-import=zeroconf._utils.ipaddress Gopro_Gui_interfase_Pyqt5.py
    ```

#### Problem: **Recording Fails to Start on All Cameras**
- **Solution**:
  - Ensure that the `goprolist_usb_activate_time_sync_record.py` script is run to synchronize all cameras before recording. This script helps ensure that commands are properly executed on all devices.

#### Problem: **"Host key verification failed" error when pushing to GitHub**
- **Solution**:
  - This happens when the SSH key has not been saved in your known_hosts file. When prompted, type `yes` to confirm the connection to GitHub.
  - Alternatively, you can delete the problematic entry from your `known_hosts` file and try connecting again.

## Use Cases

The Shramko GoPro Control App can be used in various professional and creative scenarios. Below are some examples of how the application can be used effectively in different types of projects.

### 1. Virtual Studio Productions
**Scenario**: A virtual studio needs to capture synchronized footage from multiple angles for use in background replacement and augmented reality environments.

**How to Use**:
- **Step 1**: Set up multiple GoPro Hero 10 cameras around the set to cover all angles.
- **Step 2**: Connect all cameras to the central computer using USB.
- **Step 3**: Launch the app and use the "Connect to Cameras" feature to establish connections.
- **Step 4**: Set up the desired video settings using `read_and_write_all_settings_from_prime_to_other.py` to ensure uniformity across cameras.
- **Step 5**: Start recording using the "Record" button to ensure all cameras capture footage simultaneously.
- **Step 6**: After filming, use `copy_to_pc_and_scene_sorting.py` to download and organize footage for editing.

**Benefits**:
- Synchronized recordings enable consistent and easily trackable footage for post-production.
- Saving time by using a single interface for all camera controls.

### 2. Music Video Production
**Scenario**: A music video director wants to capture different perspectives of a band performance to create dynamic shots in post-production.

**How to Use**:
- **Step 1**: Set up multiple GoPro cameras at different positions: close-ups, medium shots, and wide angles.
- **Step 2**: Run the application and use the "Set First Camera Preset" feature to apply identical settings to all cameras.
- **Step 3**: Use `sync_and_record.py` to synchronize the time and start recording in one step.
- **Step 4**: After the performance, use `copy_to_pc.py` to download all footage to your computer.
- **Step 5**: Use the "Save Log" feature to document any issues or changes during filming.

**Benefits**:
- Consistent camera settings reduce the time spent on color grading and matching shots during editing.
- Automatically sorted footage makes it easier to manage multiple takes.

### 3. Advertising Campaign with Multiple Angles
**Scenario**: An advertising team wants to create an immersive video showcasing a product from multiple viewpoints.

**How to Use**:
- **Step 1**: Position multiple GoPro cameras at strategic points around the product.
- **Step 2**: Launch the app and connect all cameras.
- **Step 3**: Use the "Record" and "Stop" buttons to precisely control the timing of the shots.
- **Step 4**: Utilize `set_video_mode.py` to adjust the settings for capturing high-resolution close-ups.
- **Step 5**: Once recording is complete, format the SD cards using `format_sd.py` to prepare the cameras for the next product shoot.

**Benefits**:
- The application allows for precise control over recording sessions, reducing human error and ensuring all perspectives are captured without manual intervention.
- Reusable settings for each camera make it easy to replicate similar shoots for different products.

### 4. Multi-Camera Coverage for Outdoor Events
**Scenario**: Filming a live event, such as a sports competition or a concert, with multiple cameras positioned at different parts of the venue.

**How to Use**:
- **Step 1**: Set up GoPro cameras at key positions, such as the start line, finish line, and audience area.
- **Step 2**: Use `goprolist_usb_activate_time_sync.py` to ensure all cameras have synchronized time settings.
- **Step 3**: During the event, use the app to record footage from all cameras simultaneously.
- **Step 4**: After the event, run `copy_to_pc_and_scene_sorting.py` to download footage and organize it by event phases.

**Benefits**:
- Time synchronization across all cameras ensures smooth editing when compiling footage from multiple perspectives.
- The ability to control all cameras simultaneously reduces the risk of missing key moments.

## Project Architecture

The Shramko GoPro Control App is designed with a modular architecture, making it easier to manage, modify, and expand the application. Below is a detailed overview of how different components are organized and how they interact with each other.

### Main Components

The project is divided into several main components:

1. **Graphical User Interface (GUI) Module**:
   - **Files**: `Gopro_Gui_interfase_Pyqt5.py`, `Gopro_Gui_Interface.py`, `status_of_cameras_GUI.py`
   - **Purpose**: These scripts provide the user interface for interacting with GoPro cameras. The GUI is implemented using **PyQt5**, which allows users to control cameras through a visual interface.
   - **Interaction**: The GUI scripts interact with the control and management scripts to send commands to the cameras, such as starting/stopping recording or synchronizing settings.

2. **Camera Management Module**:
   - **Files**: `goprolist_and_start_usb.py`, `goprolist_usb_activate_time_sync.py`, `read_and_write_all_settings_from_prime_to_other.py`
   - **Purpose**: These scripts are responsible for managing the connection and configuration of multiple GoPro cameras. They handle tasks like initializing connections, setting camera parameters, and synchronizing time.
   - **Interaction**: The camera management scripts are called by the GUI module or can be run independently to prepare the cameras for a recording session.

3. **Recording Control Module**:
   - **Files**: `recording.py`, `stop_record.py`, `sync_and_record.py`
   - **Purpose**: This module handles all recording-related operations, including starting, stopping, and synchronizing recording across multiple cameras.
   - **Interaction**: The recording scripts can be invoked from the GUI to start or stop a recording session. They use the **camera management module** to ensure all cameras are properly synchronized.

4. **File Management Module**:
   - **Files**: `copy_to_pc.py`, `copy_to_pc_and_scene_sorting.py`, `format_sd.py`
   - **Purpose**: These scripts manage the downloading and organization of footage from the cameras. They also handle SD card formatting when needed.
   - **Interaction**: After a recording session, the file management scripts are used to download footage from each camera and sort it into appropriate directories for post-production. These scripts can be run independently or triggered through the GUI.

5. **Utility and Helper Scripts**:
   - **Files**: `set_video_mode.py`, `set_preset_0.py`, `camera_orientation_lock.py`, `sleep.py`
   - **Purpose**: These utility scripts perform specific tasks, such as setting the video mode, applying presets, or adding delays between operations to prevent issues with camera commands.
   - **Interaction**: The utility scripts are often used by other modules to perform low-level operations, such as setting specific camera modes or ensuring all cameras have similar settings.

### Data Flow and Interactions

1. **Initialization Phase**:
   - The process starts by running **goprolist_and_start_usb.py**, which discovers and connects to all GoPro cameras.
   - The **camera management module** then synchronizes settings and prepares the cameras using scripts like `read_and_write_all_settings_from_prime_to_other.py`.

2. **Recording Phase**:
   - During recording, the **recording control module** is used to start and stop recording on all cameras simultaneously.
   - The **sync_and_record.py** script ensures that time is synchronized before recording starts, reducing the complexity of post-production.

3. **Post-Recording Phase**:
   - Once recording is complete, the **file management module** is used to download all footage from the cameras and sort it for editing.
   - The **format_sd.py** script can be used to clear all SD cards to prepare for the next recording session.

### Technologies Used

- **Python 3.11**: The core programming language used for the entire application.
- **PyQt5**: Used to create the graphical user interface, making the application user-friendly.
- **ZeroConf**: Utilized to discover cameras connected over USB and manage network communication between the system and GoPro cameras.
- **PyInstaller**: Used to create standalone `.exe` files for easy distribution of the application without requiring users to install Python or dependencies.
- **JSON**: The **camera_cache.json** file is used to store cached information about the cameras, making reconnections faster.

### Key Points to Understand

- **Modularity**: The project is designed to be modular. Each script focuses on a specific task (e.g., connecting cameras, downloading footage), which makes the project easier to maintain and extend.
- **Inter-module Communication**: Scripts communicate with each other through command-line arguments or by being invoked directly from the GUI. This allows for flexibility in how the user interacts with the system.
- **User Customization**: The settings and parameters used by each camera can be customized using the **primary camera** as a reference (`prime_camera_sn.py`), allowing users to easily apply identical settings across multiple devices.

## Contribution and Community Interaction

The Shramko GoPro Control App is an open-source project, and contributions are welcome! Whether it's fixing a bug, suggesting a new feature, or improving documentation, your help is greatly appreciated. Below are guidelines on how you can contribute effectively.

### How to Contribute

#### 1. Reporting Issues
If you encounter a bug or have an idea for an enhancement, you can report it by creating an **issue** in the GitHub repository.

- Go to the **Issues** tab of the [GitHub repository](https://github.com/AndriiShramko/Shramko_GoPro_Control_App/issues).
- Click on **New Issue**.
- Provide a descriptive title and detailed information about the issue:
  - **For Bugs**: Include steps to reproduce, expected behavior, actual behavior, and screenshots (if applicable).
  - **For Enhancements**: Describe the feature or enhancement you have in mind, including why it would be beneficial.

#### 2. Contributing Code via Pull Requests (PRs)
If you would like to contribute code to the project, please follow these steps:

- **Step 1: Fork the Repository**:
  - Fork the [repository](https://github.com/AndriiShramko/Shramko_GoPro_Control_App) to your own GitHub account by clicking the **Fork** button.

- **Step 2: Clone Your Fork**:
  - Clone your fork to your local machine:
    ```sh
    git clone https://github.com/YourUsername/Shramko_GoPro_Control_App.git
    cd Shramko_GoPro_Control_App
    ```

- **Step 3: Create a Branch**:
  - Create a new branch for your feature or bug fix:
    ```sh
    git checkout -b feature-or-bug-description
    ```

- **Step 4: Make Changes and Commit**:
  - Make your changes in your branch.
  - Add and commit your changes:
    ```sh
    git add .
    git commit -m "Description of changes made"
    ```

- **Step 5: Push Your Branch**:
  - Push your branch to your fork on GitHub:
    ```sh
    git push origin feature-or-bug-description
    ```

- **Step 6: Create a Pull Request**:
  - Go to your forked repository on GitHub.
  - Click on **Compare & pull request**.
  - Provide a detailed description of the changes made and submit your PR.

#### 3. Reviewing Pull Requests
If you are interested in reviewing others' contributions:
- Go to the **Pull Requests** tab of the repository.
- Review open pull requests, comment with suggestions, or approve changes.

### Code Style Guidelines

- **Python Version**: This project uses **Python 3.11**.
- **Formatting**: Follow **PEP 8** style guidelines for Python code. It's recommended to use a tool like **flake8** or **black** to automatically format your code.
- **Comments and Documentation**: Please include comments in your code to explain complex logic. Update relevant sections in the `README.md` if your changes affect the way the project is used.

### Community Standards

We value contributions of all types and are committed to providing a welcoming environment for everyone. Please adhere to the following standards:

- **Be Respectful**: Respect the time and effort that contributors put into the project. Offer constructive criticism and support other contributors.
- **Open Discussion**: Keep discussions open, transparent, and respectful. Ask questions and share insights in issues and pull requests.
- **Help Improve**: If you're not comfortable contributing code, consider helping by improving the documentation, testing, or suggesting new features.

### Contact

If you have any questions or need further guidance, feel free to reach out to Andrii Shramko via:

- **Email**: [zmei116@gmail.com](mailto:zmei116@gmail.com)
- **LinkedIn**: [Andrii Shramko](https://www.linkedin.com/in/andrii-shramko/)

