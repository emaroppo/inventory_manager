from classes.order import CustomerOrder, Product
from .db import db


class Cart:
    db = db

    @classmethod
    def from_user_id(cls, user_id):
        items = cls.db.execute(
            """SELECT product_id,qty FROM cart_items WHERE user_id=?""", (user_id,)
        ).fetchall()
        print(items)
        items = [(Product.from_id(product_id), qty) for product_id, qty in items]
        return cls(user_id, items)

    def __init__(self, user_id, items=list()) -> None:
        self.user_id = user_id
        self.items = items

    def add_item(self, product_id, qty):
        self.items.append((Product.from_id(product_id), qty))
        self.db.execute(
            """INSERT INTO cart_items (user_id, product_id, qty) VALUES (?, ?, ?)""",
            (self.user_id, product_id, qty),
        )

    def checkout(self):
        # create order
        order = CustomerOrder.add(user_id=self.user_id)
        # add items to order
        order.add_items(self.items)
        return order

    def to_json(self):
        out_json = {"user_id": self.user_id}
        items = [i[0].to_json() for i in self.items]
        out_json["items"] = []
        for i, j in zip(items, self.items):
            out_json["items"].append({"item": i, "qty": j[1]})
        print(out_json)
        return out_json
