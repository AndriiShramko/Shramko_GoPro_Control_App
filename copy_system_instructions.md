# Инструкция по реализации системы копирования файлов с GoPro камер

## 1. Структура системы

### 1.1 Основные компоненты
- `CopyManager` - главный класс управления копированием
- `FileStatistics` - класс для сбора статистики
- `CopyProgressWidget` - виджет для отображения прогресса
- Система логирования

### 1.2 Вспомогательные классы
- `FileInfo` - информация о файле
- `SceneInfo` - информация о сцене (группе файлов)
- `CopyStatistics` - статистика копирования

## 2. Процесс копирования

### 2.1 Подготовка к копированию
1. Получить список камер из camera_cache.json
2. Для каждой камеры:
   - Запросить список файлов через API (/gopro/media/list)
   - Создать объекты FileInfo для каждого файла
   - Проверить доступность камеры

### 2.2 Группировка файлов по сценам
1. Сортировать файлы по времени создания
2. Группировать файлы в сцены:
   - Интервал между файлами <= 5 минут = одна сцена
   - Создавать новую сцену при превышении интервала
3. Для каждой сцены:
   - Создать уникальное имя на основе времени
   - Подсчитать общий размер файлов
   - Создать директорию для сцены

### 2.3 Процесс копирования
1. Для каждой сцены:
   - Создать директорию сцены
   - Для каждого файла в сцене:
     * Проверить существование файла
     * Проверить размер если файл существует
     * Копировать файл с отслеживанием прогресса
     * Верифицировать скопированный файл

### 2.4 Верификация копирования
1. Проверять размер файла до и после копирования
2. Проверять доступность файла на камере
3. Проверять права доступа к директории назначения
4. Проверять свободное место на диске

## 3. Система логирования

### 3.1 Уровни логирования
- DEBUG: детальная информация для отладки
- INFO: основные операции копирования
- WARNING: некритичные проблемы
- ERROR: критические ошибки
- CRITICAL: фатальные ошибки

### 3.2 Что логировать
1. Начало/конец копирования
2. Статус каждого файла:
   - Начало копирования
   - Прогресс копирования
   - Завершение копирования
   - Ошибки копирования
3. Статистику:
   - Общее количество файлов
   - Размер файлов
   - Время копирования
   - Скорость копирования
4. Ошибки:
   - Недоступность камеры
   - Ошибки чтения/записи
   - Ошибки верификации

### 3.3 Формат лога
```
[TIMESTAMP] [LEVEL] [MODULE] Message
Дополнительная информация в нескольких строках
```

## 4. Обработка ошибок

### 4.1 Типы ошибок
1. Ошибки подключения:
   - Камера недоступна
   - Сетевые проблемы
2. Ошибки файловой системы:
   - Недостаточно места
   - Нет прав доступа
   - Файл занят
3. Ошибки данных:
   - Неверный размер файла
   - Ошибка верификации
4. Ошибки API камеры:
   - Неверный ответ
   - Таймаут

### 4.2 Обработка ошибок
1. Для каждого типа ошибки:
   - Логировать детали
   - Обновлять статус файла
   - Уведомлять пользователя
2. Стратегии восстановления:
   - Повторные попытки для сетевых ошибок
   - Пропуск проблемных файлов
   - Возможность продолжить с места сбоя

## 5. Отображение прогресса

### 5.1 Информация для отображения
1. Общий прогресс:
   - Процент выполнения
   - Оставшееся время
   - Скорость копирования
2. Прогресс по сценам:
   - Название сцены
   - Количес��во файлов
   - Статус копирования
3. Прогресс по файлам:
   - Имя файла
   - Размер
   - Статус
   - Процент выполнения
4. Статистика:
   - Всего файлов
   - Скопировано
   - Пропущено
   - Ошибки

### 5.2 Обновление GUI
1. Использовать сигналы Qt:
   - progress_updated
   - status_updated
   - error_occurred
2. Частота обновления:
   - Прогресс: каждые 100мс
   - Статистика: каждую секунду
   - Ошибки: немедленно

## 6. Оптимизация

### 6.1 Производительность
1. Многопоточное копирование:
   - ThreadPoolExecutor для параллельного копирования
   - Ограничение количества потоков
2. Размер буфера:
   - Оптимальный размер chunk_size
   - Управление памятью
3. Кэширование:
   - Кэш списка файлов
   - Кэш статистики

### 6.2 Надежность
1. Механизм восстановления:
   - Сохранение состояния копирования
   - Возможность продолжить ��рерванное копирование
2. Проверка целостности:
   - Проверка размера файлов
   - Проверка доступности файлов
3. Обработка исключений:
   - Корректное закрытие потоков
   - Освобождение ресурсов

## 7. Тестирование

### 7.1 Модульные тесты
1. Тестирование компонентов:
   - CopyManager
   - FileStatistics
   - Логирование
2. Тестирование сценариев:
   - Успешное копирование
   - Обработка ошибок
   - Отмена копирования

### 7.2 Интеграционные тесты
1. Взаимодействие с камерами
2. Работа с файловой системой
3. Обновление GUI

### 7.3 Тестовые сценарии
1. Копирование больших файлов
2. Прерывание копирования
3. Потеря связи с камерой
4. Нехватка места на диске 