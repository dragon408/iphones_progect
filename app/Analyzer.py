import sqlite3

class Analyzer:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_iphone_prices(self, iphone_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stores = ['comfy', 'foxtrot', 'moyo']  # додай ще, якщо треба
        results = []

        for store in stores:
            cursor.execute(f"""
                SELECT product_name, price, url
                FROM {store}
                WHERE product_name LIKE ?
            """, (f"%{iphone_name}%",))
            data = cursor.fetchall()

            for product_name, price, url in data:
                results.append((product_name, price, store, url))

        conn.close()
        return results
