#!/usr/bin/env python3
"""
Главное окно управления пользователями системы HelpDesk
Предоставляет интерфейс для просмотра, добавления и редактирования пользователей
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Настройка пути для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController


class UserManagementWindow(tk.Tk):
    """
    Основное окно администрирования пользователей
    Реализует CRUD-операции через графический интерфейс
    """

    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()

        # Конфигурация окна
        self.title("HelpDesk — Управление аккаунтами")
        self.geometry("1020x640")
        self.resizable(True, True)
        self.configure(bg='#2a2d3b')

        # Переменные состояния
        self.selected_user_id = None

        # Создание интерфейса
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        """Создание всех элементов UI"""
        # Заголовок
        header = tk.Frame(self, bg='#2a2d3b')
        header.pack(pady=(15, 10))

        title = tk.Label(
            header,
            text="Администрирование пользователей",
            font=('Verdana', 18, 'bold'),
            bg='#2a2d3b',
            fg='#a9def9'
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Добавление, редактирование и управление учётными записями",
            font=('Arial', 10),
            bg='#2a2d3b',
            fg='#8aa6c1'
        )
        subtitle.pack()

        # Фрейм кнопок
        btn_frame = tk.Frame(self, bg='#2a2d3b')
        btn_frame.pack(fill=tk.X, padx=20, pady=(5, 10))

        # Кнопки с единым стилем
        btn_style = {
            'font': ('Segoe UI', 10),
            'bg': '#5e678c',
            'fg': 'white',
            'relief': tk.RAISED,
            'bd': 2,
            'width': 16,
            'height': 1
        }

        self.add_button = tk.Button(btn_frame, text="Добавить", command=self.add_user, **btn_style)
        self.add_button.grid(row=0, column=0, padx=(0, 10))

        self.edit_button = tk.Button(btn_frame, text="Редактировать", command=self.edit_user, **btn_style)
        self.edit_button.grid(row=0, column=1, padx=(0, 10))

        self.remove_button = tk.Button(btn_frame, text="Деактивировать", command=self.deactivate_user, **btn_style)
        self.remove_button.grid(row=0, column=2, padx=(0, 10))

        self.status_button = tk.Button(btn_frame, text="Изменить роль", command=self.change_role, **btn_style)
        self.status_button.grid(row=0, column=3, padx=(0, 10))

        self.refresh_button = tk.Button(btn_frame, text="Обновить", command=self.load_users, **btn_style)
        self.refresh_button.grid(row=0, column=4)

        # Настройка сетки
        btn_frame.grid_columnconfigure(4, weight=1)

        # Таблица пользователей
        table_frame = tk.Frame(self, bg='#2a2d3b')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.create_table(table_frame)

        # Статус-бар
        self.status_bar = tk.Label(
            self,
            text="Загрузка...",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Segoe UI', 9),
            bg='#3c415e',
            fg='#d0e4ff'
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_table(self, parent):
        """Создание таблицы Treeview"""
        # Scrollbar
        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(parent, orient=tk.HORIZONTAL)

        # Таблица
        self.tree = ttk.Treeview(
            parent,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse',
            height=20
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Колонки
        columns = ('id', 'login', 'role', 'is_active', 'fullname')
        self.tree['columns'] = columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('id', width=60, anchor=tk.CENTER)
        self.tree.column('login', width=180, anchor=tk.W)
        self.tree.column('role', width=150, anchor=tk.W)
        self.tree.column('is_active', width=100, anchor=tk.CENTER)
        self.tree.column('fullname', width=350, anchor=tk.W)

        # Заголовки
        self.tree.heading('id', text='ID', anchor=tk.CENTER)
        self.tree.heading('login', text='Логин', anchor=tk.W)
        self.tree.heading('role', text='Роль', anchor=tk.W)
        self.tree.heading('is_active', text='Активен', anchor=tk.CENTER)
        self.tree.heading('fullname', text='ФИО', anchor=tk.W)

        # Стиль
        style = ttk.Style()
        style.configure('Treeview', rowheight=25, font=('Segoe UI', 10), background='#3c415e', foreground='white')
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#5e678c', foreground='white')
        style.map('Treeview', background=[('selected', '#5a6280')])

        # Размещение
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_users(self):
        """Загрузка списка пользователей"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            users = UserController.fetch_all()

            for user in users:
                is_active_text = 'Да' if user.is_active else 'Нет'
                self.tree.insert('', tk.END, values=(
                    user.id,
                    user.login,
                    user.role,
                    is_active_text,
                    user.fullname or ''
                ))

            self.status_bar.config(text=f"Загружено: {len(users)} пользователей")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.status_bar.config(text="Ошибка при загрузке")

    def on_select(self, event):
        """Обработка выбора строки"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_user_id = item['values'][0]
            self.status_bar.config(text=f"Выбран ID: {self.selected_user_id}")

    def get_selected_user(self):
        """Получение ID выбранного пользователя"""
        if not self.selected_user_id:
            messagebox.showwarning("Внимание", "Выберите пользователя из списка")
            return None
        return self.selected_user_id

    def add_user(self):
        """Открыть окно добавления"""
        from Views.AddUserWindow import AddUserWindow
        window = AddUserWindow(self)
        window.grab_set()
        self.wait_window(window)
        self.load_users()

    def edit_user(self):
        """Открыть окно редактирования"""
        user_id = self.get_selected_user()
        if not user_id:
            return
        from Views.EditUserWindow import EditUserWindow
        window = EditUserWindow(self, user_id)
        window.grab_set()
        self.wait_window(window)
        self.load_users()

    def deactivate_user(self):
        """Деактивировать пользователя"""
        user_id = self.get_selected_user()
        if not user_id:
            return

        if not messagebox.askyesno("Подтвердите", f"Деактивировать пользователя ID {user_id}?"):
            return

        try:
            result = UserController.modify_user(user_id, is_active=False)
            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Готово", "Пользователь деактивирован")
                self.load_users()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось деактивировать: {str(e)}")

    def change_role(self):
        """Изменить роль пользователя"""
        user_id = self.get_selected_user()
        if not user_id:
            return

        from Views.EditUserWindow import EditUserWindow
        window = EditUserWindow(self, user_id)
        window.role_combobox.focus_set()
        window.grab_set()
        self.wait_window(window)
        self.load_users()


if __name__ == "__main__":
    app = UserManagementWindow()
    app.mainloop()