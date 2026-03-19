from Models.Base import *

class KnowledgeBase(Base):
    """
        Модель базы знаний — хранит пары «вопрос-ответ».
        Поиск осуществляется по хешу текста запроса.
    """
    id = PrimaryKeyField()
    query = CharField(max_length=255) #  в виде хэша
    response = TextField() # ответ для вопроса
    text_query = CharField() # текст вопроса для теста

