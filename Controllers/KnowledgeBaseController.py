from Models.KnowledgeBase import KnowledgeBase
import hashlib


class KnowledgeBaseController:
    '''
    Контроллер для управления базой знаний.
    Добавление, поиск по хешу, удаление записей.
    '''

    @classmethod
    def get_all(cls):
        '''
        Получает все записи из базы знаний.
        :return: запрос с полной выборкой
        '''
        return KnowledgeBase.select()

    @classmethod
    def find_by_hash(cls, query_hash):
        '''
        Ищет запись по хешу запроса.
        :param query_hash: строка хеша (SHA-256)
        :return: объект записи или None
        '''
        return KnowledgeBase.get_or_none(KnowledgeBase.query == query_hash)

    @classmethod
    def add_entry(cls, text_query, response):
        '''
        Добавляет новую пару "вопрос-ответ" в базу знаний.
        Перед добавлением проверяет дубликаты по хешу.
        :param text_query: текст вопроса
        :param response: текст ответа
        :return: сообщение о результате
        '''
        query_hash = hashlib.sha256(text_query.encode('utf-8')).hexdigest()
        existing = cls.find_by_hash(query_hash)

        if existing:
            return f'Запись уже существует (ID: {existing.id})'

        try:
            KnowledgeBase.create(
                query=query_hash,
                response=response,
                text_query=text_query
            )
            return f'Добавлено: "{text_query[:30]}..."'
        except Exception as e:
            return f'Ошибка при добавлении: {str(e)}'

    @classmethod
    def remove_entry(cls, entry_id):
        '''
        Удаляет запись из базы знаний по ID.
        :param entry_id: идентификатор записи
        :return: результат операции
        '''
        try:
            record = KnowledgeBase.get_or_none(KnowledgeBase.id == entry_id)
            if not record:
                return f'Запись не найдена (ID: {entry_id})'
            record.delete_instance()
            return f'Удалено: ID {entry_id}'
        except Exception as e:
            return f'Ошибка удаления: {str(e)}'

    @classmethod
    def compute_hash(cls, text):
        '''
        Вспомогательный метод: вычисляет SHA-256 хеш строки.
        :param text: входной текст
        :return: hex-представление хеша
        '''
        return hashlib.sha256(text.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    print("=== Тест: KnowledgeBaseController ===")

    print(KnowledgeBaseController.add_entry(
        "Как сбросить пароль в 1С?",
        "Через администратора базы или восстановление через email."
    ))

    print(KnowledgeBaseController.add_entry(
        "Проблема с принтером",
        "Проверьте подключение, драйвера и очередь печати."
    ))

    print("\nВсе записи:")
    for row in KnowledgeBaseController.get_all():
        print(f"ID: {row.id}, Вопрос: {row.text_query}")

    # Пример хеширования
    print("\nХеш 'test':", KnowledgeBaseController.compute_hash("test"))