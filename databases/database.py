import sqlite3


# connection = sqlite3.connect('db.sqlite')
class Database:

    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS review_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    tg_id INTEGER,
                    genre TEXT
                )
            """)
            connection.execute("""
            CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER,
                    category TEXT
            """)

            connection.commit()

    def execution(self, sql):
        with sqlite3.connect(self.path) as connection:
            connection.execute(sql)
            connection.commit()
