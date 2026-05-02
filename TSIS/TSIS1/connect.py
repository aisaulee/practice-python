import psycopg2
from config import load_config

def connect(config):
    """ Установка соединения с сервером PostgreSQL """
    try:

        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка подключения: {error}")
        return None

if __name__ == '__main__':
    params = load_config()
    connect(params)