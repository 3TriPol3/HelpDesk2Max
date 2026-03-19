from tkinter.constants import CASCADE

from Models.Category import Category
from Models.Base import *
from Models.User import User


class Task(Base):
    """
        Модель заявки (тикета) в системе техподдержки.
        Содержит описание, статус, приоритет, автора и исполнителя.
    """
    id = PrimaryKeyField()
    topic = CharField(max_length=100)
    description = TextField()
    path = CharField(max_length=255) # путь к файлу в папке на сервере
    priority = CharField(
        choices= [
            'Низкий',
            'Средний',
            'Высокий'
        ]
    )
    status = CharField(
        choices=[
            'Новая',
            'В работе',
            'Выполнена',
            'Отклонена',
            'Ожидает ответа пользователя'
        ]
    )
    user_id = ForeignKeyField(model=User, on_delete=CASCADE,on_update=CASCADE)
    speciality_id = ForeignKeyField(model=User,on_delete=CASCADE,on_update=CASCADE, null=True)
    category_id = ForeignKeyField(model=Category,on_delete=CASCADE,on_update=CASCADE)

