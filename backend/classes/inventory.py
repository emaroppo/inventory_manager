from .db import db, conn


class Inventory:
    db = db
    conn = conn

    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path

    def add_order(self, store_id, items):
        db.execute(
            """INSERT INTO orders(store_id)
            VALUES (?)""",
            (store_id,),
        )
        self.conn.commit()
        db.execute(
            """SELECT order_id FROM orders
            WHERE store_id = ? AND status_id = 1""",
            (store_id,),
        )
        order_id = db.fetchone()

        for item in items:
            if item[2] > self.check_instore_product_availability(
                product_id=item[1], store_id=store_id
            ):
                in_stock = False
            else:
                in_stock = True

            self.db.execute(
                """INSERT INTO order_details(order_id, product_id, qty, in_stock) VALUES (?, ?, ?)""",
                (order_id[0], item[1], item[2], in_stock),
            )

        return order_id[0]

    def add_restock_order(self, store_id, items):
        self.db.execute(
            """INSERT INTO restock_orders(store_id)
            VALUES (?)""",
            (store_id,),
        )
        self.conn.commit()
        self.db.execute(
            """SELECT restock_order_id FROM restock_orders
            WHERE store_id = ? AND status_id = 1""",
            (store_id,),
        )
        restock_order_id = self.db.fetchone()

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
            self.db.execute(
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
            self.db.execute(
                """SELECT qty FROM stock
                WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                AND store_id = ?""",
                (product_name, store_id),
            )
            qty = self.db.fetchone()

        elif product_id:
            self.db.execute(
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
        for item in order.items:
            store_id, product_name, qty = item
            self.db.execute(
                """UPDATE stock SET qty = stock.qty - ?
                WHERE product_id = (SELECT product_id FROM products WHERE product_name = ?)
                AND store_id = ?""",
                (qty, product_name, store_id),
            )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
