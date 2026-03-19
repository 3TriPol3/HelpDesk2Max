from Models.Base import *

class Category(Base):
    """
       Модель категории заявки.
       Используется для классификации задач в системе.
    """
    id = PrimaryKeyField()
    name = CharField(unique=True,max_length=150)
