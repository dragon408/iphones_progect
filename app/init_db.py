# init_db.py
from db_setup import DB


def initialize_db():
    db = DB()  # Створюємо екземпляр бази даних
    # Створюємо таблиці для кожного магазину
    stores = ["rozetka", "ctrs", "foxtrot", "moyo", "comfy"]
    for store in stores:
        db.create_store_table(store)
    print("База даних та таблиці для магазинів створено!")


if __name__ == "__main__":
    initialize_db()
