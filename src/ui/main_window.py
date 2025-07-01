"""
Главное окно приложения Image Processor Pro.
Содержит пользовательский интерфейс и логику взаимодействия с пользователем.
"""

import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QWidget, QFileDialog, QComboBox, QMessageBox, QInputDialog,
                            QGroupBox, QSizePolicy, QDialog, QLineEdit, QDialogButtonBox)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QPalette, QColor, QIntValidator
from PyQt5.QtCore import Qt, QSize

class ImageLoader:
    @staticmethod
    def load_image(file_path):
        """Статический метод для загрузки изображения из файла"""
        try:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Не удалось загрузить изображение")
            return image
        except Exception as e:
            raise Exception(f"Ошибка загрузки: {str(e)}")

    @staticmethod
    def capture_from_camera():
        """Статический метод для захвата изображения с камеры"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Камера не доступна")
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise Exception("Не удалось получить кадр")
        
        return frame

class ImageProcessor:
    @staticmethod
    def extract_channel(image, channel_index):
        """Извлекает указанный цветовой канал из изображения"""
        if image is None:
            raise ValueError("Изображение не загружено")
        if channel_index == 0:  # Синий
            return cv2.merge([image[:,:,0], np.zeros_like(image[:,:,0]), np.zeros_like(image[:,:,0])])
        elif channel_index == 1:  # Зеленый
            return cv2.merge([np.zeros_like(image[:,:,0]), image[:,:,1], np.zeros_like(image[:,:,0])])
        else:  # Красный
            return cv2.merge([np.zeros_like(image[:,:,0]), np.zeros_like(image[:,:,0]), image[:,:,2]])

    @staticmethod
    def crop_image(image, x1, y1, x2, y2):
        """Обрезает изображение по заданным координатам"""
        return image[y1:y2, x1:x2]

    @staticmethod
    def adjust_brightness(image, value):
        """Регулирует яркость изображения на указанное значение"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] = np.clip(hsv[:,:,2] + value, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    @staticmethod
    def draw_circle(image, x, y, radius):
        """Рисует круг на изображении с заданными параметрами"""
        result = image.copy()
        cv2.circle(result, (x, y), radius, (0, 0, 255), 2)
        return result

class MainWindow(QMainWindow):
    """Главное окно приложения, наследуемое от QMainWindow"""
    
    def __init__(self):
        super().__init__()
        self.image = None  # Оригинальное изображение
        self.processed_image = None  # Обработанное изображение
        self.setup_fonts()  # Настройка шрифтов
        self.setup_ui()     # Настройка интерфейса
        self.setup_styles() # Настройка стилей
        
    def setup_fonts(self):
        """Инициализация шрифтов для различных элементов интерфейса"""
        self.big_font = QFont()
        self.big_font.setPointSize(16)
        
        self.title_font = QFont()
        self.title_font.setPointSize(18)
        self.title_font.setBold(True)
        
        self.button_font = QFont()
        self.button_font.setPointSize(14)

    def setup_styles(self):
        """Настройка CSS-стилей для элементов интерфейса"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QGroupBox {
                border: 2px solid #d1d5db;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: bold;
                color: #374151;
            }
            QLabel#imageLabel {
                background-color: white;
                border: 3px solid #d1d5db;
                border-radius: 8px;
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #374151;
                margin-bottom: 5px;
            }
            QPushButton {
                min-width: 250px;
                min-height: 50px;
                padding: 12px 18px;
                font-size: 14px;
                border-radius: 8px;
            }
            QComboBox {
                min-width: 250px;
                min-height: 40px;
                font-size: 14px;
                padding: 5px;
            }
        """)

    def setup_ui(self):
        """Настройка основного пользовательского интерфейса"""
        self.setWindowTitle("Image Processor Pro")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        # Левая панель (изображения)
        image_panel = QVBoxLayout()
        image_panel.setSpacing(10)

        # Оригинальное изображение
        original_title = QLabel("ОРИГИНАЛЬНОЕ ИЗОБРАЖЕНИЕ")
        original_title.setObjectName("titleLabel")
        original_title.setFont(self.title_font)
        original_title.setAlignment(Qt.AlignCenter)
        original_title.setContentsMargins(0, 0, 0, 10)
        image_panel.addWidget(original_title)

        self.image_label = QLabel()
        self.image_label.setObjectName("imageLabel")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 450)
        image_panel.addWidget(self.image_label)

        # Результат обработки
        processed_title = QLabel("РЕЗУЛЬТАТ ОБРАБОТКИ")
        processed_title.setObjectName("titleLabel")
        processed_title.setFont(self.title_font)
        processed_title.setAlignment(Qt.AlignCenter)
        processed_title.setContentsMargins(0, 20, 0, 10)
        image_panel.addWidget(processed_title)

        self.result_label = QLabel()
        self.result_label.setObjectName("imageLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumSize(600, 450)
        image_panel.addWidget(self.result_label)

        # Правая панель (управление)
        control_panel = QVBoxLayout()
        control_panel.setSpacing(25)
        control_panel.setContentsMargins(15, 15, 15, 15)

        # Группа "Загрузка изображения"
        load_group = QGroupBox("ЗАГРУЗКА ИЗОБРАЖЕНИЯ")
        load_group.setFont(self.title_font)
        load_layout = QVBoxLayout()
        
        self.load_btn = self.create_button("Загрузить из файла", "folder.png", "#4f46e5")
        self.camera_btn = self.create_button("Сделать фото", "camera.png", "#10b981")
        
        load_layout.addWidget(self.load_btn)
        load_layout.addWidget(self.camera_btn)
        load_group.setLayout(load_layout)
        control_panel.addWidget(load_group)

        # Группа "Цветовые каналы"
        channel_group = QGroupBox("ЦВЕТОВЫЕ КАНАЛЫ")
        channel_group.setFont(self.title_font)
        channel_layout = QVBoxLayout()
        
        self.channel_combo = QComboBox()
        self.channel_combo.setFont(self.button_font)
        self.channel_combo.addItems(["Синий канал", "Зеленый канал", "Красный канал"])
        
        self.show_channel_btn = self.create_button("Показать канал", "color.png", "#f59e0b")
        
        channel_layout.addWidget(self.channel_combo)
        channel_layout.addWidget(self.show_channel_btn)
        channel_group.setLayout(channel_layout)
        control_panel.addWidget(channel_group)

        # Группа "Операции с изображением"
        ops_group = QGroupBox("ОПЕРАЦИИ С ИЗОБРАЖЕНИЕМ")
        ops_group.setFont(self.title_font)
        ops_layout = QVBoxLayout()
        
        self.crop_btn = self.create_button("Обрезать", "crop.png", "#6366f1")
        self.brightness_btn = self.create_button("Яркость", "brightness.png", "#ec4899")
        self.circle_btn = self.create_button("Нарисовать круг", "circle.png", "#8b5cf6")
        
        ops_layout.addWidget(self.crop_btn)
        ops_layout.addWidget(self.brightness_btn)
        ops_layout.addWidget(self.circle_btn)
        ops_group.setLayout(ops_layout)
        control_panel.addWidget(ops_group)

        main_layout.addLayout(image_panel, 70)
        main_layout.addLayout(control_panel, 30)

        self.connect_signals()

    def create_button(self, text, icon_name=None, color="#4f46e5"):
        """Создает стилизованную кнопку с иконкой и цветом"""
        button = QPushButton(text)
        button.setFont(self.button_font)
        button.setMinimumSize(250, 50)
        
        if icon_name:
            button.setIcon(QIcon(f"icons/{icon_name}"))
            button.setIconSize(QSize(24, 24))
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 20)};
            }}
        """)
        
        return button

    def darken_color(self, hex_color, percent=10):
        """Затемняет цвет для эффектов наведения на кнопки"""
        color = QColor(hex_color)
        return color.darker(100 + percent).name()

    def connect_signals(self):
        """Подключает сигналы кнопок к соответствующим слотам"""
        self.load_btn.clicked.connect(self.load_image)
        self.camera_btn.clicked.connect(self.capture_from_camera)
        self.show_channel_btn.clicked.connect(self.show_channel)
        self.crop_btn.clicked.connect(self.crop_image_dialog)
        self.brightness_btn.clicked.connect(self.adjust_brightness_dialog)
        self.circle_btn.clicked.connect(self.draw_circle_dialog)

    def load_image(self):
        """Открывает диалог выбора файла и загружает изображение"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        
        if file_name:
            try:
                self.image = ImageLoader.load_image(file_name)
                if self.image is not None:
                    self.display_image(self.image, self.image_label)
                    self.show_message("Успех", "Изображение успешно загружено!")
            except Exception as e:
                self.show_message("Ошибка", f"Не удалось загрузить изображение: {str(e)}", True)

    def capture_from_camera(self):
        """Захватывает изображение с веб-камеры"""
        try:
            frame = ImageLoader.capture_from_camera()
            if frame is not None:
                self.image = frame
                self.display_image(self.image, self.image_label)
                self.show_message("Успех", "Фото с камеры успешно сделано!")
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка камеры: {str(e)}", True)

    def show_channel(self):
        """Отображает выбранный цветовой канал изображения"""
        if self.image is None:
            self.show_message("Предупреждение", "Сначала загрузите изображение", False)
            return
        
        channel = self.channel_combo.currentIndex()
        processed = ImageProcessor.extract_channel(self.image, channel)
        self.processed_image = processed
        self.display_image(processed, self.result_label)

    def crop_image_dialog(self):
        """Открывает диалог для обрезки изображения"""
        if self.image is None:
            self.show_message("Предупреждение", "Сначала загрузите изображение", False)
            return
        
        try:
            height, width = self.image.shape[:2]
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Обрезка изображения")
            dialog.setFixedSize(550, 350)
            
            layout = QVBoxLayout()
            
            input_style = """
                QLineEdit {
                    font-size: 16px;
                    padding: 12px;
                    min-width: 120px;
                }
                QLabel {
                    font-size: 16px;
                }
            """
            
            def create_input(label_text, default_val, max_val):
                hbox = QHBoxLayout()
                label = QLabel(label_text)
                label.setFont(self.big_font)
                input = QLineEdit(str(default_val))
                input.setFont(self.big_font)
                input.setValidator(QIntValidator(0, max_val))
                input.setStyleSheet(input_style)
                hbox.addWidget(label)
                hbox.addWidget(input)
                return hbox, input
            
            # Ограничения для обрезки
            max_dim = max(width, height)
            x1_layout, x1_input = create_input("X начальной точки (0-{}):".format(width-1), 0, width-1)
            y1_layout, y1_input = create_input("Y начальной точки (0-{}):".format(height-1), 0, height-1)
            x2_layout, x2_input = create_input("X конечной точки (1-{}):".format(width), 1, width)
            y2_layout, y2_input = create_input("Y конечной точки (1-{}):".format(height), 1, height)
            
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.setFont(self.big_font)
            
            layout.addLayout(x1_layout)
            layout.addLayout(y1_layout)
            layout.addLayout(x2_layout)
            layout.addLayout(y2_layout)
            layout.addWidget(button_box)
            dialog.setLayout(layout)
            
            def accept():
                try:
                    x1 = int(x1_input.text())
                    y1 = int(y1_input.text())
                    x2 = int(x2_input.text())
                    y2 = int(y2_input.text())
                    
                    if x1 >= x2 or y1 >= y2:
                        raise ValueError("Начальные координаты должны быть меньше конечных")
                    if (x2 - x1) < 10 or (y2 - y1) < 10:
                        raise ValueError("Минимальный размер области обрезки - 10x10 пикселей")
                    
                    self.processed_image = ImageProcessor.crop_image(self.image, x1, y1, x2, y2)
                    self.display_image(self.processed_image, self.result_label)
                    dialog.accept()
                except Exception as e:
                    self.show_message("Ошибка", f"Неверные координаты: {str(e)}", True)
            
            button_box.accepted.connect(accept)
            button_box.rejected.connect(dialog.reject)
            
            dialog.exec_()
            
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка обрезки: {str(e)}", True)

    def adjust_brightness_dialog(self):
        """Открывает диалог для настройки яркости"""
        if self.image is None:
            self.show_message("Предупреждение", "Сначала загрузите изображение", False)
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Настройка яркости")
        dialog.setFixedSize(450, 200)
        
        layout = QVBoxLayout()
        
        label = QLabel("Введите значение яркости (0-100):")
        label.setFont(self.big_font)
        
        input = QLineEdit("20")
        input.setFont(self.big_font)
        input.setValidator(QIntValidator(0, 100))
        input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 12px;
            }
        """)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setFont(self.big_font)
        
        layout.addWidget(label)
        layout.addWidget(input)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        def accept():
            try:
                value = int(input.text())
                if value < 0 or value > 100:
                    raise ValueError("Значение должно быть от 0 до 100")
                
                self.processed_image = ImageProcessor.adjust_brightness(self.image, value)
                self.display_image(self.processed_image, self.result_label)
                dialog.accept()
            except Exception as e:
                self.show_message("Ошибка", f"Не удалось изменить яркость: {str(e)}", True)
        
        button_box.accepted.connect(accept)
        button_box.rejected.connect(dialog.reject)
        
        dialog.exec_()

    def draw_circle_dialog(self):
        """Открывает диалог для рисования круга на изображении"""
        if self.image is None:
            self.show_message("Предупреждение", "Сначала загрузите изображение", False)
            return
        
        try:
            height, width = self.image.shape[:2]
            max_radius = min(width, height) // 2
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Рисование круга")
            dialog.setFixedSize(500, 300)
            
            layout = QVBoxLayout()
            
            def create_input(label_text, default_val, max_val):
                hbox = QHBoxLayout()
                label = QLabel(label_text)
                label.setFont(self.big_font)
                input = QLineEdit(str(default_val))
                input.setFont(self.big_font)
                input.setValidator(QIntValidator(0, max_val))
                input.setStyleSheet("""
                    QLineEdit {
                        font-size: 16px;
                        padding: 12px;
                    }
                """)
                hbox.addWidget(label)
                hbox.addWidget(input)
                return hbox, input
            
            # Ограничения для круга
            x_layout, x_input = create_input("X центра (0-{}):".format(width-1), width//2, width-1)
            y_layout, y_input = create_input("Y центра (0-{}):".format(height-1), height//2, height-1)
            r_layout, r_input = create_input("Радиус (1-{}):".format(max_radius), min(width, height)//8, max_radius)
            
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.setFont(self.big_font)
            
            layout.addLayout(x_layout)
            layout.addLayout(y_layout)
            layout.addLayout(r_layout)
            layout.addWidget(button_box)
            dialog.setLayout(layout)
            
            def accept():
                try:
                    x = int(x_input.text())
                    y = int(y_input.text())
                    radius = int(r_input.text())
                    
                    if radius <= 0:
                        raise ValueError("Радиус должен быть положительным числом")
                    if x - radius < 0 or x + radius >= width or y - radius < 0 or y + radius >= height:
                        raise ValueError("Круг выходит за границы изображения")
                    
                    self.processed_image = ImageProcessor.draw_circle(self.image, x, y, radius)
                    self.display_image(self.processed_image, self.result_label)
                    dialog.accept()
                except Exception as e:
                    self.show_message("Ошибка", f"Неверные параметры круга: {str(e)}", True)
            
            button_box.accepted.connect(accept)
            button_box.rejected.connect(dialog.reject)
            
            dialog.exec_()
            
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка рисования: {str(e)}", True)

    def show_message(self, title, message, is_error=False):
        """Показывает сообщение пользователю"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setFont(self.big_font)
        
        if is_error:
            msg.setIcon(QMessageBox.Critical)
        else:
            msg.setIcon(QMessageBox.Information)
            
        msg.exec_()

    def display_image(self, image, label):
        """Отображает изображение в QLabel"""
        try:
            if image is None:
                raise ValueError("Нет изображения для отображения")

            if len(image.shape) == 3:
                if image.shape[2] == 3:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                elif image.shape[2] == 4:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
                else:
                    raise ValueError(f"Неожиданное число каналов: {image.shape[2]}")
            else:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(
                label.width(), 
                label.height(), 
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            label.setPixmap(pixmap)
            
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка отображения: {str(e)}", True)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())