import sqlite3


# connection = sqlite3.connect('db.sqlite')
class Database:

    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    tg_id INTEGER
                    )
            """)
            connection.execute("""
            CREATE TABLE IF NOT EXISTS review_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone_number INTEGER,
                    food_rating INTEGER,
                    cleanliness_rating INTEGER,
                    extra_comments TEXT,
                    tg_id INTEGER,
                    date DATE
                    )
            """)
            connection.execute("""
            CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER,
                    category_id INTEGER REFERENCES dish_categories(id)
                    )
            """)
            connection.execute("""
            CREATE TABLE IF NOT EXISTS dish_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                    )
            """)
            connection.commit()

    def execution(self, sql, parameters=None):
        with sqlite3.connect(self.path) as connection:
            if parameters is not None:
                connection.execute(sql, parameters)
            else:
                connection.execute(sql)
            connection.commit()

    def fetch(self, sql, parameters=None):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            if parameters is not None:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)
            data = cursor.fetchall()
            return data
