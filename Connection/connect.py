from peewee import *

def connect():
    try: # удачная попытка
        database = MySQLDatabase(
            'HelpDesk2Max',
            user='HelpDesk2Max',
            password='111111',
            host='localhost'
        )
        return database
    except : # неудачная попытка
        print(f'Ошибка')
        return None

if __name__ ==  "__main__":
    print(connect().connect())

