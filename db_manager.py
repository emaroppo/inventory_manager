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

    c.execute(
        """CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY,
            store_id INTEGER NOT NULL,
            fulfilled BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (store_id) REFERENCES stores(store_id)
            ON UPDATE CASCADE
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS order_details(
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCE store(store_id)
        ON UPDATE CASCADE
        FOREIGN KEY (product_id) REFERENCE products(product_id) ON UPDATE CASCADE,
        UNIQUE (order_id, product_id)
    )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS restock_orders(restock_order_id INTEGER PRIMARY KEY,
            store_id INTEGER NOT NULL,
            fulfilled BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (store_id) REFERENCES stores(store_id)
            ON UPDATE CASCADE)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS restock_order_details(restock_order_id INTEGER NOT NULL,
        store_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        received BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (restock_order_id) REFERENCE restock_orders(restock_order_id)"""
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

    def add_order(self, store_id, items):
        self.c.execute(
            """INSERT INTO orders(store_id)
            VALUES (?)""",
            (store_id,),
        )
        self.conn.commit()
        self.c.execute(
            """SELECT order_id FROM orders
            WHERE store_id = ? AND fulfilled = 0""",
            (store_id,),
        )
        order_id = self.c.fetchone()

        for item in items:
            self.c.execute(
                """INSERT INTO order_details(order_id, product_id, qty) VALUES (?, ?, ?)""",
                (order_id, item[1], item[2]),
            )

        return order_id[0]

    def add_restock_order(self, store_id, items):
        self.c.execute(
            """INSERT INTO restock_orders(store_id)
            VALUES (?)""",
            (store_id,),
        )
        self.conn.commit()
        self.c.execute(
            """SELECT restock_order_id FROM restock_orders
            WHERE store_id = ? AND fulfilled = 0""",
            (store_id,),
        )
        restock_order_id = self.c.fetchone()

        for item in items:
            self.c.execute(
                """INSERT INTO restock_order_details(restock_order_id, product_id, qty) VALUES (?, ?, ?)""",
                (restock_order_id, item[1], item[2]),
            )

        return restock_order_id[0]

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

    def check_instore_product_availability(self, product_name, store_id):
        self.c.execute(
            """SELECT qty FROM stock
            WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
            AND store_id = ?""",
            (product_name, store_id),
        )
        qty = self.c.fetchone()
        if qty is None:
            return 0
        else:
            return qty[0]

    def fulfill_order(self, order):
        # for item in the order, if the store_id and product_id are in stock, update the qty by subtracting the new qty from the old qty
        try:
            for item in order.items:
                store_id, product_name, qty = item
                self.c.execute(
                    """UPDATE stock SET qty = stock.qty - ?
                    WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                    AND store_id = ?""",
                    (qty, product_name, store_id),
                )
            self.conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            out_of_stock = [
                i[1]
                for i in order.items
                if self.check_instore_product_availability(i[0], i[1]) < int(i[2])
            ]
            print(f"Out of stock: {', '.join(out_of_stock)}")

    def __del__(self):
        self.conn.close()
