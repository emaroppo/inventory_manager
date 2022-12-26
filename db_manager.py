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
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    def add_category(self, category_name):
        self.c.execute(
            """INSERT INTO categories(category_name)
            VALUES (?)""",
            (category_name,),
        )
        self.conn.commit()

    def add_product(self, product_name, category_name):

        self.c.execute(
            """INSERT INTO products(product_name, category_id)
            VALUES (?, (SELECT category_id FROM categories WHERE category_name = ?))""",
            (product_name, category_name),
        )
        self.conn.commit()
        self.conn.close()

    def add_store(self, street_n, street_name, city, ZIP):
        try:
            self.c.execute(
                """INSERT INTO stores(street_n, street_name, city, ZIP)
                VALUES (?, ?, ?, ?)""",
                (street_n, street_name, city, ZIP),
            )
        except sqlite3.IntegrityError:
            print("Store already exists")
        self.conn.commit()

    def restock(self, restock_file):
        # read restock_file
        with open(restock_file, "r") as f:
            restock_lines = f.read().splitlines()

        # for each line in restock_file, if the store_id and product_id are not in stock, add them, otherwise update the qty by adding the new qty to the old qty

        for line in restock_lines:
            store_id, product_name, qty = line.split(",")
            self.c.execute(
                """INSERT INTO stock(product_id, store_id, qty)
                VALUES ((SELECT product_id FROM products WHERE product_name = ?), ?, ?)
                ON CONFLICT (product_id, store_id) DO UPDATE SET qty = stock.qty + ?""",
                (product_name, store_id, qty, qty),
            )
        self.conn.commit()
        self.conn.close()

    def fulfill_order(self, order_file="restock.csv"):
        # read order_file
        with open(order_file, "r") as f:
            order_lines = f.read().splitlines()

        # for each line in order_file, if the store_id and product_id are in stock, update the qty by subtracting the new qty from the old qty
        try:
            for line in order_lines:
                store_id, product_name, qty = line.split(",")
                self.c.execute(
                    """UPDATE stock SET qty = stock.qty - ?
                    WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                    AND store_id = ?""",
                    (qty, product_name, store_id),
                )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"{product_name}: Not enough stock")

        except sqlite3.OperationalError:
            print(f"{product_name}: Product not in stock")

    def __del__(self):
        self.conn.close()


# TO DO: impelement check for qty in stock for all items in the order before fulfilling order
