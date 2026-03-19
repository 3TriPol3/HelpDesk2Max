#!/usr/bin/env python3
"""
Окно добавления нового пользователя в систему HelpDesk
Модальное окно для ввода данных нового пользователя
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController


class AddUserWindow(tk.Toplevel):
    """
    Окно для добавления нового пользователя
    Наследуется от tk.Toplevel для создания модального диалогового окна
    """

    def __init__(self, parent):
        """
        Инициализация окна добавления пользователя

        Args:
            parent: родительское окно (UserManagementWindow)
        """
        super().__init__(parent)

        # Настройка окна
        self.title("Создание учётной записи")
        self.geometry("460x500")
        self.resizable(False, False)
        self.configure(bg='#2a2d3b')

        # Сохраняем ссылку на родительское окно
        self.parent = parent

        # Установка модального режима
        self.transient(parent)
        self.grab_set()

        # Инициализация переменных формы
        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.role_var = tk.StringVar(value="Пользователь")
        self.fullname_var = tk.StringVar()

        # Создание виджетов
        self.create_widgets()

        # Фокусировка на первом поле
        self.login_entry.focus_set()

        # Привязка события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def create_widgets(self):
        """Создание всех виджетов формы добавления пользователя"""

        # Заголовок сверху с центрированием
        title_frame = tk.Frame(self, bg='#2a2d3b')
        title_frame.pack(pady=(35, 15))

        title_label = tk.Label(
            title_frame,
            text="Новый пользователь",
            font=('Verdana', 17, 'bold'),
            bg='#2a2d3b',
            fg='#a9def9'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Заполните данные для регистрации",
            font=('Arial', 9),
            bg='#2a2d3b',
            fg='#8aa6c1'
        )
        subtitle_label.pack()

        # Основной фрейм формы
        form_frame = tk.Frame(self, bg='#2a2d3b')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 15))

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
            fg='white',
            selectbackground='#5a6280',
            selectforeground='white'
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

        # Пароль
        tk.Label(
            form_frame,
            text="Пароль:",
            font=('Segoe UI', 10),
            bg='#2a2d3b',
            fg='#d0e4ff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 6))

        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=('Segoe UI', 11),
            width=26,
            show="•",
            bd=1,
            relief=tk.SOLID,
            bg='#3c415e',
            fg='white',
            selectbackground='#5a6280',
            selectforeground='white'
        )
        self.password_entry.pack(pady=(0, 12), ipady=5)

        # Подтверждение пароля
        tk.Label(
            form_frame,
            text="Подтвердите:",
            font=('Segoe UI', 10),
            bg='#2a2d3b',
            fg='#d0e4ff',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 6))

        self.confirm_password_entry = tk.Entry(
            form_frame,
            textvariable=self.confirm_password_var,
            font=('Segoe UI', 11),
            width=26,
            show="•",
            bd=1,
            relief=tk.SOLID,
            bg='#3c415e',
            fg='white',
            selectbackground='#5a6280',
            selectforeground='white'
        )
        self.confirm_password_entry.pack(pady=(0, 12), ipady=5)

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
            fg='white',
            selectbackground='#5a6280',
            selectforeground='white'
        )
        self.fullname_entry.pack(pady=(0, 16), ipady=5)

        # Кнопки — внизу, горизонтально
        button_frame = tk.Frame(self, bg='#2a2d3b')
        button_frame.pack(pady=(0, 25))

        self.add_button = tk.Button(
            button_frame,
            text="Зарегистрировать",
            command=self.add_user,
            font=('Segoe UI', 10, 'bold'),
            bg='#5e678c',
            fg='white',
            activebackground='#727fa0',
            activeforeground='white',
            relief=tk.RAISED,
            bd=2,
            width=18,
            height=2
        )
        self.add_button.grid(row=0, column=0, padx=(0, 18))

        self.cancel_button = tk.Button(
            button_frame,
            text="Отмена",
            command=self.cancel,
            font=('Segoe UI', 10),
            bg='#4a4a5a',
            fg='white',
            activebackground='#5a5a6a',
            activeforeground='white',
            relief=tk.RAISED,
            bd=2,
            width=10,
            height=2
        )
        self.cancel_button.grid(row=0, column=1)

        # Настройка сетки кнопок
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Привязка горячих клавиш
        self.bind('<Return>', lambda event: self.add_user())
        self.bind('<Escape>', lambda event: self.cancel())

    def validate_form(self):
        """
        Валидация данных формы

        Returns:
            True если данные валидны, False в противном случае
        """
        login = self.login_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
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

        if not password:
            messagebox.showwarning("Ошибка", "Введите пароль")
            self.password_entry.focus_set()
            return False

        if password != confirm_password:
            messagebox.showwarning("Ошибка", "Пароли не совпадают")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
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

    def add_user(self):
        """Добавление нового пользователя в систему"""
        if not self.validate_form():
            return

        login = self.login_var.get().strip()
        password = self.password_var.get()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip() or None

        try:
            result = UserController.register(
                login=login,
                password=password,
                role=role
            )

            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                users = UserController.fetch_all()
                new_user = next((u for u in users if u.login == login), None)
                if new_user and fullname:
                    UserController.modify_user(new_user.id, fullname=fullname)

                messagebox.showinfo("Готово", f"Пользователь {login} добавлен")
                self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить: {str(e)}")

    def cancel(self):
        """Отмена добавления пользователя и закрытие окна"""
        if messagebox.askyesno("Подтвердите", "Отменить создание?"):
            self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = AddUserWindow(root)
    app.mainloop()