import sqlite3
import reader


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
                status_id INTEGER NOT NULL DEFAULT 1,
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
                status_id INTEGER NOT NULL,
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

    def update_stores_table(self, stores):
        for store in stores:
            self.add_store(store.street_n, store.street_name, store.city, store.ZIP)

    def update_products_table(self, products):
        for product in products:
            self.add_product(product.product_name, product.category_name)

    def setup_example_db(self):
        self.setup_db()
        stores = reader.stores_from_csv("examples/stores.csv")
        with open("examples/categories.csv", "r") as f:
            categories = f.read().splitlines()
            for category in categories:
                self.add_category(category)

        self.update_stores_table(stores)
        products = reader.products_from_csv("examples/products.csv")
        self.update_products_table(products)

    def __del__(self):
        self.conn.close()


class Inventory:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    def add_order(self, store_id, items):
        self.c.execute(
            """INSERT INTO orders(store_id)
            VALUES (?)""",
            (store_id,),
        )
        self.conn.commit()
        self.c.execute(
            """SELECT order_id FROM orders
            WHERE store_id = ? AND status_id = 1""",
            (store_id,),
        )
        order_id = self.c.fetchone()

        for item in items:
            if item[2] > self.check_instore_product_availability(
                product_id=item[1], store_id=store_id
            ):
                in_stock = False
            else:
                in_stock = True

            self.c.execute(
                """INSERT INTO order_details(order_id, product_id, qty, in_stock) VALUES (?, ?, ?)""",
                (order_id[0], item[1], item[2], in_stock),
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
            WHERE store_id = ? AND status_id = 1""",
            (store_id,),
        )
        restock_order_id = self.c.fetchone()

        for item in items:
            self.c.execute(
                """INSERT INTO restock_order_details(restock_order_id, product_id, qty) VALUES (?, ?, ?)""",
                (restock_order_id[0], item[1], item[2]),
            )

        return restock_order_id[0]

    def restock(self, order):

        # for each line in restock_file, if the store_id and product_id are not in stock, add them, otherwise update the qty by adding the new qty to the old qty

        for item in order.items:
            store_id, product_name, qty = item
            self.c.execute(
                """INSERT INTO stock(product_id, store_id, qty)
                VALUES ((SELECT product_id FROM products WHERE product_name = ?), ?, ?)
                ON CONFLICT (product_id, store_id) DO UPDATE SET qty = stock.qty + ?""",
                (product_name, store_id, qty, qty),
            )
        self.conn.commit()

    def check_instore_product_availability(
        self, store_id, product_name=None, product_id=None
    ):

        if product_id and product_name:
            raise TypeError("Specify only 1 of product_id and product_name")

        if product_name:
            self.c.execute(
                """SELECT qty FROM stock
                WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                AND store_id = ?""",
                (product_name, store_id),
            )
            qty = self.c.fetchone()

        elif product_id:
            self.c.execute(
                """SELECT qty FROM stock WHERE product_id = ? AND store_id= ?""",
                (product_id, store_id),
            )

        else:
            raise TypeError("Specify at least 1 of product_id and product_name")

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
