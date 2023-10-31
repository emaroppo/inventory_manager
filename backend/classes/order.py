from .db import db
from .product import Product

class Order:
    db = db

    @classmethod
    def add(cls, store_id, order_items):
        cls.db.execute(
            "INSERT INTO orders (store_id) VALUES (?)",
            (store_id,),
        )
        order_id = cls.db.lastrowid
        for item in order_items:
            cls.db.execute(
                "INSERT INTO order_items (order_id, product_id, qty, shipped) VALUES (?, ?, ?, ?)",
                (order_id, item[0].product_id, item[1], item[2]),
            )
        cls.db.commit()
        return order_id
    def __init__(self, order_id):
        self.order_id = order_id
    
class Restock(Order):
    def __init__(self, store_id, items):
        super().__init__(store_id)
        self.products=items

class Purchase(Order):
    def __init__(self, order_id, partial=True):
        super().__init__(order_id)
        order, order_items = self.db.retrieve_order(order_id)

        self.store_id, self.status_id= order
        self.items = [(Product(product_id=i[0]),i[1], i[2]) for i in order_items]
        self.available_items = [i for i in self.items if i[0].in_stock(self.store_id, i[1])]
        self.shippable_items = [i for i in self.available_items if not i[2]]
        self.partial = partial