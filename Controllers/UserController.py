from Models.User import User
from bcrypt import hashpw, gensalt, checkpw


class UserController:
    '''
    Контроллер управления пользователями системы.
    Регистрация, аутентификация, обновление данных.
    '''

    @classmethod
    def fetch_all(cls):
        '''
        Возвращает всех пользователей из базы.
        :return: запрос с выборкой всех записей
        '''
        return User.select()

    @classmethod
    def register(cls, login, password, role='Пользователь'):
        '''
        Регистрирует нового пользователя с хешированием пароля.
        :param login: логин (до 12 символов, уникальный)
        :param password: пароль (будет захеширован)
        :param role: роль при создании
        :return: сообщение об успехе или ошибке
        '''
        if len(login) > 12:
            return 'Ошибка: логин не должен превышать 12 символов'

        try:
            hashed = hashpw(password.encode('utf-8'), gensalt())
            User.create(
                login=login,
                password=hashed.decode('utf-8'),
                role=role
            )
            return f'Пользователь {login} добавлен'
        except Exception as e:
            return f'Ошибка регистрации: {str(e)}'

    @classmethod
    def modify_user(cls, user_id, **fields):
        '''
        Обновляет данные пользователя по ID.
        :param user_id: идентификатор записи
        :param fields: поля и новые значения (например: login="new_login")
        :return: результат операции
        '''
        allowed_fields = {'login', 'role', 'fullname', 'is_active'}
        for field in fields:
            if field not in allowed_fields:
                return f'Нельзя изменить поле: {field}'

        try:
            query = User.update(**fields).where(User.id == user_id)
            query.execute()
            return f'Данные пользователя ID {user_id} обновлены'
        except Exception as e:
            return f'Ошибка обновления: {str(e)}'

    @classmethod
    def toggle_status(cls, user_id):
        '''
        Переключает статус активности пользователя.
        :param user_id: ID пользователя
        :return: сообщение с новым статусом
        '''
        user = User.get_or_none(User.id == user_id)
        if not user:
            return 'Пользователь не найден'

        new_status = not user.is_active
        User.update(is_active=new_status).where(User.id == user_id).execute()
        return f'Статус изменён на {new_status}'

    @classmethod
    def authenticate(cls, login, password):
        '''
        Аутентифицирует пользователя по логину и паролю.
        :param login: имя пользователя
        :param password: пароль
        :return: словарь с данными при успехе, иначе строка ошибки
        '''
        user = User.get_or_none(User.login == login)
        if not user:
            return 'Неверный логин или пароль'

        if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {
                'status': 'success',
                'user': {
                    'id': user.id,
                    'login': user.login,
                    'role': user.role,
                    'fullname': user.fullname,
                    'is_active': user.is_active
                }
            }
        return 'Неверный логин или пароль'


if __name__ == "__main__":
    print("=== Тест: UserController ===")

    print(UserController.register(login='user', password='user'))
    print(UserController.register(login='admin', password='admin', role='Администратор'))

    print("\nВсе пользователи:")
    for u in UserController.fetch_all():
        print(f" - {u.id}: {u.login} | {u.role} | Активен: {u.is_active}")

    print(UserController.toggle_status(1))
    print(UserController.modify_user(1, fullname="Иван Иванов"))

    auth_result = UserController.authenticate('user', 'user')
    if isinstance(auth_result, dict):
        print(f"Вход выполнен: {auth_result['user']['login']}")
    else:
        print(f"Ошибка: {auth_result}")
