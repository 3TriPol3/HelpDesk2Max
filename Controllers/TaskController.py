from Models.Task import Task
from Models.User import User
from Models.Category import Category


class TaskController:
    '''
    Контроллер для управления заявками в системе.
    Реализует создание, фильтрацию, обновление и анализ задач.
    '''

    @classmethod
    def fetch_all(cls):
        '''
        Возвращает все заявки из системы.
        :return: запрос с полной выборкой
        '''
        return Task.select()

    @classmethod
    def find_by_id(cls, task_id):
        '''
        Находит заявку по уникальному идентификатору.
        :param task_id: ID заявки
        :return: объект или None
        '''
        return Task.get_or_none(Task.id == task_id)

    @classmethod
    def get_by_user(cls, user_id):
        '''
        Получает заявки, созданные пользователем.
        :param user_id: ID автора
        :return: список заявок
        '''
        return Task.select().where(Task.user_id == user_id)

    @classmethod
    def get_by_specialist(cls, specialist_id):
        '''
        Возвращает заявки, назначенные специалисту.
        :param specialist_id: ID специалиста
        :return: список задач
        '''
        return Task.select().where(Task.specialist_id == specialist_id)

    @classmethod
    def get_active(cls):
        '''
        Возвращает активные заявки (не "Выполнена").
        :return: список активных задач
        '''
        return Task.select().where(Task.status != 'Выполнена')

    @classmethod
    def add_task(cls, title, desc, user_id, cat_id, priority='Средний', status='Новая', file_path=None):
        '''
        Создаёт новую заявку в системе.
        Перед созданием проверяет существование пользователя и категории.
        :param title: тема заявки
        :param desc: описание проблемы
        :param user_id: ID пользователя
        :param cat_id: ID категории
        :param priority: приоритет
        :param status: начальный статус
        :param file_path: путь к файлу (опционально)
        :return: результат операции
        '''
        try:
            user = User.get_or_none(User.id == user_id)
            category = Category.get_or_none(Category.id == cat_id)

            if not user:
                return 'Ошибка: пользователь не найден'
            if not category:
                return 'Ошибка: категория не найдена'

            Task.create(
                topic=title,
                description=desc,
                user_id=user_id,
                category_id=cat_id,
                priority=priority,
                status=status,
                path=file_path or '',
                specialist_id=None
            )
            return f'Заявка "{title}" добавлена'
        except Exception as e:
            return f'Ошибка при создании: {str(e)}'

    @classmethod
    def modify_task(cls, task_id, **fields):
        '''
        Обновляет поля заявки.
        :param task_id: ID задачи
        :param fields: словарь полей для изменения
        :return: сообщение о результате
        '''
        try:
            query = Task.update(**fields).where(Task.id == task_id)
            query.execute()
            return f'Задача ID {task_id} обновлена'
        except Exception as e:
            return f'Ошибка обновления: {str(e)}'

    @classmethod
    def remove_task(cls, task_id):
        '''
        Удаляет заявку по ID.
        :param task_id: идентификатор задачи
        :return: результат операции
        '''
        try:
            task = cls.find_by_id(task_id)
            if not task:
                return f'Заявка не найдена (ID: {task_id})'
            task.delete_instance()
            return f'Удалено: заявка {task_id}'
        except Exception as e:
            return f'Ошибка удаления: {str(e)}'

    @classmethod
    def update_status(cls, task_id, new_status):
        '''
        Изменяет статус заявки.
        :param task_id: ID задачи
        :param new_status: новый статус
        :return: результат
        '''
        valid_statuses = ['Новая', 'В работе', 'Выполнена', 'Отклонена', 'Ожидает ответа пользователя']
        if new_status not in valid_statuses:
            return f'Неверный статус. Допустимые: {", ".join(valid_statuses)}'

        try:
            Task.update(status=new_status).where(Task.id == task_id).execute()
            return f'Статус изменён на "{new_status}"'
        except Exception as e:
            return f'Ошибка смены статуса: {str(e)}'

    @classmethod
    def assign_to_specialist(cls, task_id, spec_id):
        '''
        Назначает специалиста на заявку.
        :param task_id: ID задачи
        :param spec_id: ID специалиста
        :return: результат
        '''
        try:
            task = cls.find_by_id(task_id)
            specialist = User.get_or_none(User.id == spec_id)

            if not task:
                return 'Заявка не найдена'
            if not specialist:
                return 'Специалист не найден'

            Task.update(specialist_id=spec_id).where(Task.id == task_id).execute()
            return f'Специалист {specialist.login} назначен'
        except Exception as e:
            return f'Ошибка назначения: {str(e)}'

    @classmethod
    def take_in_progress(cls, task_id, spec_id):
        '''
        Специалист берёт заявку в работу.
        :param task_id: ID задачи
        :param spec_id: ID специалиста
        :return: результат
        '''
        try:
            task = cls.find_by_id(task_id)
            if not task:
                return 'Заявка не найдена'

            Task.update(
                specialist_id=spec_id,
                status='В работе'
            ).where(Task.id == task_id).execute()

            return f'Заявка "{task.topic}" взята в работу'
        except Exception as e:
            return f'Ошибка при взятии в работу: {str(e)}'

    @classmethod
    def filter_by_params(cls, status=None, priority=None, category_id=None, user_id=None, specialist_id=None):
        '''
        Фильтрует заявки по заданным параметрам.
        :param status: фильтр по статусу
        :param priority: по приоритету
        :param category_id: по категории
        :param user_id: по пользователю
        :param specialist_id: по исполнителю
        :return: отфильтрованный запрос
        '''
        query = Task.select()

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if category_id:
            query = query.where(Task.category_id == category_id)
        if user_id:
            query = query.where(Task.user_id == user_id)
        if specialist_id:
            query = query.where(Task.specialist_id == specialist_id)

        return query

    @classmethod
    def get_stats(cls):
        '''
        Возвращает статистику по заявкам.
        :return: словарь с количеством задач по статусам
        '''
        total = Task.select().count()
        new = Task.select().where(Task.status == 'Новая').count()
        in_progress = Task.select().where(Task.status == 'В работе').count()
        completed = Task.select().where(Task.status == 'Выполнена').count()

        return {
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'completed': completed
        }


if __name__ == "__main__":
    print("=== Тест: TaskController ===")

    print(TaskController.add_task(
        title="Доступ к 1С",
        desc="Не открывается база данных",
        user_id=1,
        cat_id=1,
        priority="Высокий"
    ))

    print("\nВсе заявки:")
    for t in TaskController.fetch_all():
        print(f" - {t.id}: {t.topic} | {t.status}")

    print(TaskController.update_status(1, "В работе"))
    print(TaskController.assign_to_specialist(1, 2))

    stats = TaskController.get_stats()
    print(f"\nСтатистика: всего={stats['total']}, новые={stats['new']}, в работе={stats['in_progress']}")