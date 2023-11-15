from .db import db, conn
from .product import OrderItem, Product


class Order:
    db = db
    conn = conn

    def __init__(self, order_id, status_id=0):
        self.order_id = order_id
        self.status_id = status_id
        self.items = list()


class CustomerOrder(Order):
    @classmethod
    def from_id(cls, order_id):
        args = cls.db.execute(
            """SELECT * FROM customer_orders WHERE order_id=?""", (order_id,)
        ).fetchone()
        order = cls(*args)
        return order

    @classmethod
    def add(cls, user_id):
        cls.db.execute(
            "INSERT INTO customer_orders (user_id) VALUES (?)",
            (user_id,),
        )

        cls.conn.commit()
        return cls.from_id(cls.db.lastrowid)

    @classmethod
    def search(cls, user_id):
        results = cls.db.execute(
            """SELECT * FROM customer_orders WHERE user_id=?""", (user_id,)
        ).fetchall()
        results = [cls(*result) for result in results]
        return results

    def __init__(self, order_id, user_id, status_id=0):
        super().__init__(order_id, status_id)
        self.user_id = user_id

    def add_items(self, items):
        items = [
            OrderItem(product, qty, order_id=self.order_id)
            for product, qty in items
        ]
        print(items)
        print(self.items)
        self.items += items
        #insert into order_items
        for item in items:
            self.db.execute(
                """INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)""",
                (self.order_id, item.product.product_id, item.qty),
            )
    def to_json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "status_id": self.status_id,
            "items": [item.to_json() for item in self.items],
        }


class RestockOrder(Order):
    @classmethod
    def from_id(cls, order_id):
        args = cls.db.execute(
            """SELECT * FROM restock_orders WHERE restock_order_id=?""", (order_id,)
        ).fetchone()
        order = cls(*args)
        return order

    def __init__(self, order_id, store_id, items=list()):
        super().__init__(order_id, items)
        self.store_id = store_id
