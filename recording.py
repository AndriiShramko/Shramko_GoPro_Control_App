# Copyright (c) 2024 Andrii Shramko
# Contact: zmei116@gmail.com
# LinkedIn: https://www.linkedin.com/in/andrii-shramko/
# Tags: #ShramkoVR #ShramkoCamera #ShramkoSoft
# License: This code is free to use for non-commercial projects.
# For commercial use, please contact Andrii Shramko at the above email or LinkedIn.

import requests
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Thread
from goprolist_and_start_usb import discover_gopro_devices
from utils import get_app_root, get_data_dir, setup_logging, check_dependencies

# Инициализируем логирование с именем модуля
logger = setup_logging(__name__)

def start_recording_synchronized(devices):
    """Синхронный старт записи на всех камерах с использованием барьера"""
    barrier = Barrier(len(devices))
    
    def record_camera(camera_ip):
        try:
            logger.info(f"Camera {camera_ip} waiting for synchronized start")
            barrier.wait()  # Ждем, пока все камеры будут готовы
            
            start_time = time.time()
            response = requests.get(f"http://{camera_ip}:8080/gopro/camera/shutter/start", timeout=5)
            end_time = time.time()
            
            if response.status_code == 200:
                logger.info(f"Camera {camera_ip} started at {start_time:.6f}, response at {end_time:.6f}")
                return True
            else:
                logger.error(f"Failed to start camera {camera_ip}. Status: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error starting camera {camera_ip}: {e}")
            return False

    # Запускаем потоки для каждой камеры
    threads = []
    for device in devices:
        thread = Thread(target=record_camera, args=(device['ip'],))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

def save_devices_to_cache(devices, cache_filename="camera_cache.json"):
    """Сохранение списка камер в кэш"""
    try:
        cache_file = get_data_dir() / cache_filename
        with open(cache_file, "w") as file:
            json.dump(devices, file)
        logger.info("Camera devices cached successfully.")
    except Exception as e:
        logger.error(f"Failed to save camera cache: {e}")

if __name__ == "__main__":
    try:
        check_dependencies()
        devices = discover_gopro_devices()
        if devices:
            logger.info("Found the following GoPro devices:")
            for device in devices:
                logger.info(f"Name: {device['name']}, IP: {device['ip']}")

            save_devices_to_cache(devices)

            # Запускаем запись синхронно на всех камерах
            logger.info("Starting synchronized recording on all cameras...")
            start_recording_synchronized(devices)
        else:
            logger.error("No GoPro devices found.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if getattr(sys, 'frozen', False):
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка при записи")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        raise
