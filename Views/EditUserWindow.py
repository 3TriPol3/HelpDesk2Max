#!/usr/bin/env python3
"""
Окно редактирования существующего пользователя в системе HelpDesk
Модальное окно для изменения данных пользователя
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController
from Models.User import User


class EditUserWindow(tk.Toplevel):
    """
    Окно для редактирования существующего пользователя
    Наследуется от tk.Toplevel для создания модального диалогового окна
    """

    def __init__(self, parent, user_id):
        """
        Инициализация окна редактирования пользователя

        Args:
            parent: родительское окно (UserManagementWindow)
            user_id: ID редактируемого пользователя
        """
        super().__init__(parent)

        # Настройка окна
        self.title(f"Редактировать ID: {user_id}")
        self.geometry("460x480")
        self.resizable(False, False)
        self.configure(bg='#2a2d3b')

        # Сохраняем ссылку на родительское окно и ID пользователя
        self.parent = parent
        self.user_id = user_id

        # Установка модального режима
        self.transient(parent)
        self.grab_set()

        # Инициализация переменных формы
        self.login_var = tk.StringVar()
        self.role_var = tk.StringVar()
        self.fullname_var = tk.StringVar()

        # Загрузка данных пользователя
        self.user_data = self.load_user_data()
        if not self.user_data:
            messagebox.showerror("Ошибка", f"Пользователь с ID {user_id} не найден")
            self.destroy()
            return

        # Заполнение переменных данными пользователя
        self.login_var.set(self.user_data.login)
        self.role_var.set(self.user_data.role)
        self.fullname_var.set(self.user_data.fullname or "")

        # Создание виджетов
        self.create_widgets()

        # Фокусировка на первом поле
        self.login_entry.focus_set()

        # Привязка события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def load_user_data(self):
        """
        Загрузка данных пользователя по ID

        Returns:
            Объект пользователя или None, если пользователь не найден
        """
        try:
            user = User.get_or_none(User.id == self.user_id)
            return user
        except Exception as e:
            print(f"Ошибка загрузки данных пользователя: {e}")
            return None

    def create_widgets(self):
        """Создание всех виджетов формы редактирования пользователя"""

        # Заголовок
        title_frame = tk.Frame(self, bg='#2a2d3b')
        title_frame.pack(pady=(30, 10))

        title_label = tk.Label(
            title_frame,
            text="Редактирование профиля",
            font=('Verdana', 17, 'bold'),
            bg='#2a2d3b',
            fg='#a9def9'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text=f"ID: {self.user_id}",
            font=('Arial', 9),
            bg='#2a2d3b',
            fg='#8aa6c1'
        )
        subtitle_label.pack()

        # Основной фрейм формы
        form_frame = tk.Frame(self, bg='#2a2d3b')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(15, 15))

        # Логин
        tk.Label(
            form_frame,
            text="Логин:",
            font=('Segoe UI', 10),
            bg='#2a2d3b',
            fg='#d0e4ff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 6))

        self.login_entry = tk.Entry(
            form_frame,
            textvariable=self.login_var,
            font=('Segoe UI', 11),
            width=26,
            bd=1,
            relief=tk.SOLID,
            bg='#3c415e',
            fg='white'
        )
        self.login_entry.pack(pady=(0, 12), ipady=5)

        # Подсказка под логином
        hint_login = tk.Label(
            form_frame,
            text="макс. 12 символов",
            font=('Arial', 7),
            bg='#2a2d3b',
            fg='#6c7a93'
        )
        hint_login.pack(anchor='w', pady=(0, 6))

        # Роль
        tk.Label(
            form_frame,
            text="Роль:",
            font=('Segoe UI', 10),
            bg='#2a2d3b',
            fg='#d0e4ff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 6))

        self.role_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.role_var,
            values=["Пользователь", "Специалист", "Администратор"],
            font=('Segoe UI', 10),
            state="readonly",
            width=24
        )
        self.role_combobox.pack(pady=(0, 14), ipady=2)

        # Полное имя
        tk.Label(
            form_frame,
            text="ФИО:",
            font=('Segoe UI', 10),
            bg='#2a2d3b',
            fg='#d0e4ff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 6))

        self.fullname_entry = tk.Entry(
            form_frame,
            textvariable=self.fullname_var,
            font=('Segoe UI', 11),
            width=26,
            bd=1,
            relief=tk.SOLID,
            bg='#3c415e',
            fg='white'
        )
        self.fullname_entry.pack(pady=(0, 16), ipady=5)

        # Кнопки — внизу
        button_frame = tk.Frame(self, bg='#2a2d3b')
        button_frame.pack(pady=(0, 25))

        self.save_button = tk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_changes,
            font=('Segoe UI', 10, 'bold'),
            bg='#5e678c',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=16,
            height=2
        )
        self.save_button.grid(row=0, column=0, padx=(0, 18))

        self.cancel_button = tk.Button(
            button_frame,
            text="Отмена",
            command=self.cancel,
            font=('Segoe UI', 10),
            bg='#4a4a5a',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=10,
            height=2
        )
        self.cancel_button.grid(row=0, column=1)

        # Настройка сетки
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Привязка горячих клавиш
        self.bind('<Return>', lambda event: self.save_changes())
        self.bind('<Escape>', lambda event: self.cancel())

    def validate_form(self):
        """
        Валидация данных формы

        Returns:
            True если данные валидны, False в противном случае
        """
        login = self.login_var.get().strip()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip()

        if not login:
            messagebox.showwarning("Ошибка", "Введите логин")
            self.login_entry.focus_set()
            return False

        if len(login) > 12:
            messagebox.showwarning("Ошибка", "Логин ≤ 12 симв.")
            self.login_entry.focus_set()
            return False

        if role not in ["Пользователь", "Специалист", "Администратор"]:
            messagebox.showwarning("Ошибка", "Выберите роль")
            self.role_combobox.focus_set()
            return False

        if fullname and len(fullname) > 150:
            messagebox.showwarning("Ошибка", "ФИО ≤ 150 симв.")
            self.fullname_entry.focus_set()
            return False

        return True

    def save_changes(self):
        """Сохранение изменений данных пользователя"""
        if not self.validate_form():
            return

        login = self.login_var.get().strip()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip() or None

        update_data = {}

        if login != self.user_data.login:
            update_data['login'] = login

        if role != self.user_data.role:
            update_data['role'] = role

        current_fullname = self.user_data.fullname or ""
        new_fullname = fullname or ""
        if new_fullname != current_fullname:
            update_data['fullname'] = fullname

        if not update_data:
            messagebox.showinfo("Готово", "Нет изменений")
            self.destroy()
            return

        try:
            result = UserController.modify_user(self.user_id, **update_data)

            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Готово", "Данные обновлены")
                self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

    def cancel(self):
        """Отмена редактирования и закрытие окна"""
        if messagebox.askyesno("Подтвердите", "Отменить изменения?"):
            self.destroy()


if __name__ == "__main__":
    # Тестовый запуск
    root = tk.Tk()
    root.withdraw()
    from Models.User import User

    test_user = User.select().first()
    if test_user:
        app = EditUserWindow(root, test_user.id)
        app.mainloop()
    else:
        print("Нет пользователей для тестирования")
