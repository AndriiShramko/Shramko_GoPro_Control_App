ECHO is on.
# Shramko GoPro Control App

**Shramko GoPro Control App** is a powerful software solution designed for synchronizing and managing multiple GoPro Hero 10 cameras via USB. The application is capable of controlling up to 100 cameras, allowing users to start/stop recording, adjust settings, synchronize time, and download files, all from a central interface.

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

