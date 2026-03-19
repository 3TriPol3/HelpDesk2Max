#!/usr/bin/env python3
"""
Точка входа в приложение HelpDesk
Запускает графический интерфейс управления пользователями
"""

import sys
import os
import tkinter.messagebox as messagebox


# Настройка пути для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Views.UserView import UserManagementWindow
from Connection.connect import connect


def main():
    """
    Основная функция запуска приложения.
    Проверяет подключение к БД, инициализирует главное окно.
    """
    # Попытка подключения к базе данных
    db = connect()
    if not db:
        error_msg = "Не удалось подключиться к базе данных"
        print(f"{error_msg}")
        messagebox.showerror("Ошибка", error_msg)
        return 1

    try:
        db.connect()
        print("Подключение к базе установлено")
    except Exception as e:
        error_msg = f"Ошибка соединения: {e}"
        print(f"{error_msg}")
        messagebox.showerror("Ошибка подключения", error_msg)
        return 1

    # Запуск главного окна
    try:
        app = UserManagementWindow()
        print("Интерфейс запущен...")
        app.mainloop()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        messagebox.showerror("Сбой", f"Приложение аварийно завершилось.\n{e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())