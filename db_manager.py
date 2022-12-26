import sqlite3


def setup_db(db_path="inventory.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL UNIQUE)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS stores(
        store_id INTEGER PRIMARY KEY,
        street_n TEXT NOT NULL,
        street_name TEXT NOT NULL,
        city TEXT NOT NULL,
        ZIP INTEGER NOT NULL,
        UNIQUE (street_n, street_name, city, ZIP))"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS stock(
        product_id INTEGER NOT NULL,
        store_id INTEGER NOT NULL,
        qty INTEGER NOT NULL CHECK (qty >= 0),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE,
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
        ON UPDATE CASCADE,
        UNIQUE (product_id, store_id))"""
    )

    conn.commit()
    conn.close()


class Inventory:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path

    def add_category(self, category_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """INSERT INTO categories(category_name)
            VALUES (?)""",
            (category_name,),
        )
        conn.commit()
        conn.close()

    def add_product(self, product_name, category_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """INSERT INTO products(product_name, category_id)
            VALUES (?, (SELECT category_id FROM categories WHERE category_name = ?))""",
            (product_name, category_name),
        )
        conn.commit()
        conn.close()

    def add_store(self, street_n, street_name, city, ZIP):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute(
                """INSERT INTO stores(street_n, street_name, city, ZIP)
                VALUES (?, ?, ?, ?)""",
                (street_n, street_name, city, ZIP),
            )
        except sqlite3.IntegrityError:
            print("Store already exists")
        conn.commit()
        conn.close()

    def add_stock(self, product_name, store_id, qty):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """INSERT INTO stock(product_id, store_id, qty)
            VALUES ((SELECT product_id FROM products WHERE product_name = ?), ?, ?)""",
            (product_name, store_id, qty),
        )
        conn.commit()
        conn.close()

    def update_stock(self, product_name, store_id, qty):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute(
                """UPDATE stock
                SET qty = ?
                WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                AND store_id = ?""",
                (qty, product_name, store_id),
            )
        except sqlite3.OperationalError:
            print("Product not in store")
        except sqlite3.IntegrityError:
            print("Product out of stock")
        conn.commit()
        conn.close()
