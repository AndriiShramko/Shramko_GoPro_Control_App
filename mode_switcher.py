# Copyright (c) 2024 Andrii Shramko
# This code includes portions of GoPro API code licensed under MIT License.
# Copyright (c) 2017 Konrad Iturbe

import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabBar
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QFont
import asyncio
import aiohttp
import logging
import threading
from utils import setup_logging, get_data_dir
from goprolist_and_start_usb import discover_gopro_devices, reset_and_enable_usb_control

logger = setup_logging(__name__)

class ModeSwitcher(QWidget):
    modeChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.devices = []  # Кэшируем список камер
        self.discovery_thread = None
        self.initUI()
        self.loadLastMode()
        self.startDeviceDiscovery()
        
    def startDeviceDiscovery(self):
        """Запускаем поиск камер в фоне"""
        if self.discovery_thread and self.discovery_thread.is_alive():
            return
            
        self.discovery_thread = threading.Thread(target=self._discover_devices_thread)
        self.discovery_thread.daemon = True
        self.discovery_thread.start()
        
    def _discover_devices_thread(self):
        """Поиск камер в отдельном потоке"""
        try:
            self.devices = discover_gopro_devices()
            if not self.devices:
                logger.warning("No GoPro devices found")
            else:
                logger.info(f"Found {len(self.devices)} GoPro devices")
                # Активируем USB для каждой найденной камеры
                for device in self.devices:
                    try:
                        reset_and_enable_usb_control(device['ip'])
                    except Exception as e:
                        logger.error(f"Failed to enable USB for camera {device['name']}: {e}")
        except Exception as e:
            logger.error(f"Error discovering devices: {e}")
            self.devices = []
            
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tabBar = QTabBar()
        self.tabBar.setExpanding(True)
        self.tabBar.setDrawBase(False)
        
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.tabBar.setFont(font)
        
        self.tabBar.addTab("VIDEO")
        self.tabBar.addTab("PHOTO")
        self.tabBar.addTab("TIMELAPSE")
        
        self.tabBar.setFixedHeight(50)
        
        self.tabBar.setStyleSheet("""
            QTabBar::tab {
                background: #2b2b2b;
                color: #808080;
                border: none;
                padding: 15px 20px;
                min-width: 100px;
                max-width: 200px;
            }
            QTabBar::tab:selected {
                background: #404040;
                color: white;
            }
            QTabBar::tab:hover {
                background: #353535;
            }
        """)
        
        layout.addWidget(self.tabBar)
        
        self.tabBar.currentChanged.connect(self._handleTabChange)
        
        self.tabToMode = {
            0: 'video',
            1: 'photo',
            2: 'timelapse'
        }
        self.modeToTab = {v: k for k, v in self.tabToMode.items()}
        
    def _handleTabChange(self, index):
        mode = self.tabToMode[index]
        self.setMode(mode, save=True)
        
    def setMode(self, mode, save=True):
        if mode not in self.modeToTab:
            return
            
        self.tabBar.blockSignals(True)
        self.tabBar.setCurrentIndex(self.modeToTab[mode])
        self.tabBar.blockSignals(False)
        
        if save:
            self.saveLastMode(mode)
            if not self.devices:  # Если нет списка камер, запускаем поиск
                self.startDeviceDiscovery()
            thread = threading.Thread(target=self._apply_mode_thread, args=(mode,))
            thread.start()
            
        self.modeChanged.emit(mode)

    def _apply_mode_thread(self, mode):
        """Поток для применения режима"""
        if not self.devices:
            logger.error("No GoPro devices found")
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._apply_mode_async(self.devices, mode))
        finally:
            loop.close()

    async def _apply_mode_async(self, devices, mode):
        try:
            # Даем время на инициализацию USB
            await asyncio.sleep(1)
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for device in devices:
                    url = f"http://{device['ip']}:8080/gp/gpControl/command/mode?p="
                    if mode == 'video':
                        url += "0"
                    elif mode == 'photo':
                        url += "1"
                    elif mode == 'timelapse':
                        url += "13"
                        
                    tasks.append(self.set_mode_for_camera(session, url, device, mode))

                results = await asyncio.gather(*tasks, return_exceptions=True)

                success = True
                for device, result in zip(devices, results):
                    if isinstance(result, Exception):
                        logger.error(f"Error setting {mode} mode for {device['name']}: {result}")
                        success = False
                    elif not result:
                        success = False

                if success:
                    logger.info(f"Successfully set {mode} mode for all cameras")
                else:
                    logger.error(f"Failed to set {mode} mode for some cameras")

        except Exception as e:
            logger.error(f"Error applying {mode} mode: {e}")

    async def set_mode_for_camera(self, session, url, device, mode):
        try:
            async with session.get(url, timeout=2) as response:
                if response.status != 200:
                    logger.error(f"Failed to set {mode} mode for camera {device['name']}. Status: {response.status}")
                    return False
                    
            await asyncio.sleep(0.5)  # Уменьшаем задержку
            
            status_url = f"http://{device['ip']}:8080/gp/gpControl/status"
            async with session.get(status_url, timeout=2) as status_response:
                if status_response.status == 200:
                    status_data = await status_response.json()
                    current_mode = status_data.get('status', {}).get('43')
                    expected_mode = {'video': 0, 'photo': 1, 'timelapse': 13}[mode]
                    
                    if current_mode == expected_mode:
                        logger.info(f"{mode.capitalize()} mode set successfully for camera {device['name']}")
                        return True
                    else:
                        logger.error(f"Failed to verify {mode} mode for camera {device['name']}. Current mode: {current_mode}")
                        return False
                        
            return True
        except Exception as e:
            logger.error(f"Error setting {mode} mode for camera {device['name']}: {e}")
            return False
            
    def saveLastMode(self, mode):
        try:
            config_dir = get_data_dir()
            config_file = config_dir / 'last_mode.json'
            
            with open(config_file, 'w') as f:
                json.dump({'mode': mode}, f)
                
            logger.info(f"Saved last mode: {mode}")
        except Exception as e:
            logger.error(f"Error saving last mode: {e}")
            
    def loadLastMode(self):
        try:
            config_dir = get_data_dir()
            config_file = config_dir / 'last_mode.json'
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    self.setMode(data.get('mode', 'video'), save=False)
            else:
                self.setMode('video', save=False)
                
        except Exception as e:
            logger.error(f"Error loading last mode: {e}")
            self.setMode('video', save=False)

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    widget = ModeSwitcher()
    widget.setMinimumWidth(350)
    widget.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 