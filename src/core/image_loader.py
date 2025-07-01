"""
Модуль для загрузки изображений из файлов и с камеры.
Реализует обработку ошибок и конвертацию между разными форматами изображений.
"""

import cv2
import numpy as np
from PyQt5.QtWidgets import QMessageBox

class ImageLoader:
    @staticmethod
    def load_image(path):
        """
        Загружает изображение из файла с обработкой ошибок.
        
        Args:
            path (str): Путь к файлу изображения
            
        Returns:
            numpy.ndarray: Загруженное изображение в формате BGR (3 канала)
            None: В случае ошибки
        """
        try:
            print(f"Попытка загрузить: {path}")  # Логирование
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                raise ValueError("Не удалось загрузить изображение. Возможные причины:\n"
                               "1. Файл поврежден\n"
                               "2. Неподдерживаемый формат\n"
                               "3. Нет прав доступа")
            
            print(f"Успешно загружено. Размер: {image.shape}, Тип: {image.dtype}")  # Логирование
            
            # Конвертация в 3-канальное изображение при необходимости
            if len(image.shape) == 2:  # Grayscale
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif image.shape[2] == 4:  # RGBA
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
                
            return image
            
        except Exception as e:
            error_msg = f"Ошибка загрузки: {str(e)}"
            print(error_msg)  # В консоль
            QMessageBox.critical(None, "Ошибка", error_msg)
            return None

    @staticmethod
    def capture_from_camera():
        """
        Захватывает изображение с веб-камеры.
        
        Returns:
            numpy.ndarray: Кадр с камеры в формате BGR
            None: В случае ошибки
        """
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Камера недоступна. Проверьте:\n"
                               "1. Подключение камеры\n"
                               "2. Разрешения приложения\n"
                               "3. Закрытые другие программы, использующие камеру")
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                raise Exception("Не удалось получить кадр с камеры")
                
            return frame
            
        except Exception as e:
            error_msg = f"Ошибка камеры: {str(e)}"
            print(error_msg)
            QMessageBox.critical(None, "Ошибка", error_msg)
            return None