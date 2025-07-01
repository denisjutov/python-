"""
Модуль для обработки изображений с использованием OpenCV.
Содержит статические методы для различных операций с изображениями.
"""

import cv2
import numpy as np

class ImageProcessor:
    @staticmethod
    def extract_channel(image, channel):
        """
        Извлекает цветовой канал из изображения.
        
        Args:
            image (numpy.ndarray): Входное изображение BGR
            channel (int): 0-синий, 1-зеленый, 2-красный
            
        Returns:
            numpy.ndarray: Изображение с выделенным каналом
        """
        zeros = np.zeros_like(image[:, :, 0])
        if channel == 0:  # Синий
            return cv2.merge([image[:, :, 0], zeros, zeros])
        elif channel == 1:  # Зеленый
            return cv2.merge([zeros, image[:, :, 1], zeros])
        else:  # Красный
            return cv2.merge([zeros, zeros, image[:, :, 2]])

    @staticmethod
    def crop_image(image, x1, y1, x2, y2):
        """
        Обрезает изображение по заданным координатам.
        
        Args:
            image (numpy.ndarray): Входное изображение
            x1, y1 (int): Координаты верхнего левого угла
            x2, y2 (int): Координаты нижнего правого угла
            
        Returns:
            numpy.ndarray: Обрезанное изображение
        """
        return image[y1:y2, x1:x2]

    @staticmethod
    def adjust_brightness(image, value):
        """
        Регулирует яркость изображения.
        
        Args:
            image (numpy.ndarray): Входное изображение
            value (int): Значение изменения яркости (0-100)
            
        Returns:
            numpy.ndarray: Изображение с измененной яркостью
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    @staticmethod
    def draw_circle(image, x, y, radius):
        """
        Рисует круг на изображении.
        
        Args:
            image (numpy.ndarray): Входное изображение
            x, y (int): Координаты центра круга
            radius (int): Радиус круга
            
        Returns:
            numpy.ndarray: Изображение с нарисованным кругом
        """
        result = image.copy()
        cv2.circle(result, (x, y), radius, (0, 0, 255), 2)
        return result