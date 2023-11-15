from classes.order import CustomerOrder, Product
from .db import db, conn


class Cart:
    db = db
    conn = conn

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
        # check if item already in cart
        for item in self.items:
            if item[0].product_id == product_id:
                item = (item[0], item[1] + qty)
                self.db.execute(
                    """UPDATE cart_items SET qty=? WHERE user_id=? AND product_id=?""",
                    (item[1], self.user_id, product_id),
                )
                return

        # if not, add item to cart
        self.items.append((Product.from_id(product_id), qty))
        self.db.execute(
            """INSERT INTO cart_items (user_id, product_id, qty) VALUES (?, ?, ?)""",
            (self.user_id, product_id, qty),
        )
        self.conn.commit()

    def remove_item(self, product_id, qty):
        # if qty=='all' or qty>=item qty delete item, else update qty
        if qty == "all":
            self.items = [
                item for item in self.items if item[0].product_id != product_id
            ]
            self.db.execute(
                """DELETE FROM cart_items WHERE user_id=? AND product_id=?""",
                (self.user_id, product_id),
            )
            self.conn.commit()
            return

        for item in self.items:
            if item[0].product_id == product_id:
                item = (item[0], item[1] - qty)
                # if qty<=0, delete item

                if item[1] <= 0:
                    self.items = [
                        item for item in self.items if item[0].product_id != product_id
                    ]
                    self.db.execute(
                        """DELETE FROM cart_items WHERE user_id=? AND product_id=?""",
                        (self.user_id, product_id),
                    )
                    self.conn.commit()
                    return
                else:
                    self.db.execute(
                        """UPDATE cart_items SET qty=? WHERE user_id=? AND product_id=?""",
                        (item[1], self.user_id, product_id),
                    )
                    self.conn.commit()
                    return

    def checkout(self):
        # create order
        order = CustomerOrder.add(user_id=self.user_id)
        # add items to order
        order.add_items(self.items)
        # empty cart
        self.items = []
        self.db.execute(
            """DELETE FROM cart_items WHERE user_id=?""", (self.user_id,)
        )
        self.conn.commit()
        return order

    def to_json(self):
        out_json = {"user_id": self.user_id}
        items = [i[0].to_json() for i in self.items]
        out_json["items"] = []
        for i, j in zip(items, self.items):
            out_json["items"].append({"item": i, "qty": j[1]})
        return out_json
