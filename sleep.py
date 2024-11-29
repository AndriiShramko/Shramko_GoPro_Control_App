import requests
import time

# Настройка параметров
camera_ip = "172.29.143.51"  # Пример IP камеры (замените на реальный IP)
port = 8080

# URL для команд
power_down_url = f"http://{camera_ip}:{port}/gopro/camera/setting?setting=59&option=6"  # Установить спящий режим через 15 минут
keep_alive_url = f"http://{camera_ip}:{port}/gopro/camera/keep_alive"
start_recording_url = f"http://{camera_ip}:{port}/gopro/camera/shutter/start"

# Переводим камеру в спящий режим
response = requests.get(power_down_url)
if response.status_code == 200:
    print("Камера переведена в режим ожидания через 15 минут.")
else:
    print("Ошибка при попытке установить режим ожидания.")

# Отправка keep-alive сигнала для предотвращения полного выключения
for _ in range(4):
    time.sleep(1)  # Отправляем keep-alive каждые секунды, чтобы камера оставалась активной
    response = requests.get(keep_alive_url)
    if response.status_code == 200:
        print("Keep-alive команда отправлена успешно.")
    else:
        print("Ошибка при отправке keep-alive команды.")

# Задержка на 4 секунды перед началом записи
print("Ожидание 4 секунды перед началом записи...")
time.sleep(4)

# Включаем запись на камере
response = requests.get(start_recording_url)
if response.status_code == 200:
    print("Запись началась успешно.")
else:
    print("Ошибка при попытке начать запись.")
