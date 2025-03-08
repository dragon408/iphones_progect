# db_setup.py
import sqlite3
import json
from datetime import datetime


class DB:
    def __init__(self, db_name="settings/stores.db"):
        # Підключення до бази даних
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_store_table(self, store):
        # Створюємо таблицю для кожного магазину
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {store} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                product_key TEXT UNIQUE,
                price REAL,
                date TEXT,
                url TEXT
            )
        """)
        self.conn.commit()

    def post(self, store, product_name, product_key, price, url):
        # Додаємо нові дані в таблицю конкретного магазину
        self.create_store_table(store)  # Переконуємося, що таблиця існує
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Вставка або оновлення запису
        self.cursor.execute(f"""
            INSERT OR REPLACE INTO {store} (product_name, product_key, price, date, url)
            VALUES (?, ?, ?, ?, ?)
        """, (product_name, product_key, price, date, url))

        self.conn.commit()

    def get(self, store, product_key):
        # Отримуємо дані для конкретного продукту та магазину
        self.cursor.execute(f"""
            SELECT * FROM {store} WHERE product_key = ?
        """, (product_key,))
        return self.cursor.fetchone()

    def get_all_from_store(self, store):
        # Отримуємо всі дані для конкретного магазину
        self.cursor.execute(f"""
            SELECT * FROM {store}
        """)
        return self.cursor.fetchall()

    def get_price_history(self, store, product_key):
        # Отримуємо історію цін для конкретного продукту в конкретному магазині
        self.cursor.execute(f"""
            SELECT price, date FROM {store} WHERE product_key = ?
        """, (product_key,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
