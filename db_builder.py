import sqlite3
import classes

class DBBuilder:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def set_up_tables(self):

        # create product categories table

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL UNIQUE)"""
        )

        #create products table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            ON UPDATE CASCADE)"""
        )

        # create stores table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS stores(
            store_id INTEGER PRIMARY KEY,
            street_n TEXT NOT NULL,
            street_name TEXT NOT NULL,
            city TEXT NOT NULL,
            ZIP INTEGER NOT NULL,
            UNIQUE (street_n, street_name, city, ZIP))"""
        )

        # create stock table
        self.c.execute(
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

        # create orders table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY,
                store_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (store_id) REFERENCES stores(store_id)
                ON UPDATE CASCADE,
                FOREIGN KEY (status_id) REFERENCES status(status_id) ON UPDATE CASCADE 
            )"""
        )
        # create order details table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS order_details(
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            in_stock BOOLEAN NOT NULL,
            shipped BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCE store(store_id)
            ON UPDATE CASCADE,
            FOREIGN KEY (product_id) REFERENCE products(product_id) ON UPDATE CASCADE,
            UNIQUE (order_id, product_id)
        )"""
        )
        # create restock orders table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS restock_orders(restock_order_id INTEGER PRIMARY KEY,
                store_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (store_id) REFERENCES stores(store_id)
                ON UPDATE CASCADE,
                FOREIGN KEY (status_id) REFERENCES status(status_id) ON UPDATE CASCADE)"""
        )

        # create restock order details table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS restock_order_details(restock_order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            received BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (restock_order_id) REFERENCE restock_orders(restock_order_id)"""
        )

        # create status table
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS status(
                status_id INTEGER PRIMARY KEY,
                status TEXT NOT NULL
            )"""
        )

        self.conn.commit()

    def __del__(self):
        self.conn.close()
