"""
Главный файл приложения Image Processor Pro.
Создает экземпляр QApplication и главного окна, запускает цикл обработки событий.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    # Создание экземпляра QApplication (обязательно для любого PyQt5 приложения)
    app = QApplication(sys.argv)
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    # Запуск основного цикла обработки событий
    sys.exit(app.exec_())