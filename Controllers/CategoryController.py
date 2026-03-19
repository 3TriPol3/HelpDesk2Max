from Models.Category import Category


class CategoryController:
    '''
    Класс для управления категориями в системе.
    Реализует операции: добавление, изменение, удаление, получение.
    '''

    @classmethod
    def fetch_all(cls):
        '''
        Возвращает все категории из базы данных.
        :return: объект запроса с выборкой всех категорий
        '''
        return Category.select()

    @classmethod
    def find_by_id(cls, category_id):
        '''
        Находит категорию по её идентификатору.
        :param category_id: ID категории
        :return: объект категории или None
        '''
        return Category.get_or_none(Category.id == category_id)

    @classmethod
    def add(cls, title):
        '''
        Добавляет новую категорию с указанным названием.
        :param title: наименование категории
        :return: строка-результат операции
        '''
        try:
            Category.create(name=title)
            return f'Добавлено: "{title}"'
        except Exception as e:
            return f'Ошибка при создании: {str(e)}'

    @classmethod
    def modify(cls, category_id, **fields):
        '''
        Обновляет данные категории по ID.
        :param category_id: ID записи
        :param fields: поля и новые значения (например, name="Новое имя")
        :return: сообщение о результате
        '''
        try:
            query = Category.update(**fields).where(Category.id == category_id)
            query.execute()
            return f'Категория ID {category_id} обновлена'
        except Exception as e:
            return f'Ошибка обновления: {str(e)}'

    @classmethod
    def remove(cls, category_id):
        '''
        Удаляет категорию из системы.
        :param category_id: ID удаляемой категории
        :return: результат операции
        '''
        try:
            category = cls.find_by_id(category_id)
            if not category:
                return f'Категория не найдена (ID: {category_id})'
            category.delete_instance()
            return f'Удалено: ID {category_id}'
        except Exception as e:
            return f'Ошибка удаления: {str(e)}'


if __name__ == "__main__":
    print("=== Тест: CategoryManager ===")

    print(CategoryController.add("Проблемы с 1С"))
    print(CategoryController.add("Настройка почты"))
    print(CategoryController.add("Оборудование"))

    print("\nСписок категорий:")
    for cat in CategoryController.fetch_all():
        print(f" - {cat.id}: {cat.name}")

    print(CategoryController.modify(1, name="1С: Ошибка входа"))

    updated_cat = CategoryController.find_by_id(1)
    if updated_cat:
        print(f"\nОбновлено: {updated_cat.name}")

    # print(CategoryController.remove(3))