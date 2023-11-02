from .db import db


class Product:
    db = db

    @classmethod
    def from_id(cls, product_id):
        args = cls.db.execute(
            """SELECT * FROM products WHERE product_id=?""", (product_id,)
        ).fetchone()
        product = cls(*args)
        return product

    @classmethod
    def add(cls, product_name, category_id):
        cls.db.execute(
            """INSERT INTO products (product_name, category_id) VALUES (?,?)""",
            (product_name, category_id),
        )
        return cls.db.lastrowid

    @classmethod
    def search(cls, filters, page=0, per_page=0, to_json=False):
        """Filters should be a list of dictionaries s.t.
        [{store_id:1, category_id:1}, {store_id:3, category_id:2}] results in:
        (store_id=1 AND category_id=1) OR (store_id=3 AND category_id=2)"""
        if filters:
            query = """SELECT * FROM products WHERE """
            for i, filter in enumerate(filters):
                if i > 0:
                    query += """ OR """
                for j, key in enumerate(filter):
                    if j > 0:
                        query += """ AND """
                    query += f"""{key}=?"""
            sql_query = """SELECT * FROM products WHERE product_id IN (SELECT product_id FROM stock WHERE store_id=?) AND category_id=?"""

        else:
            sql_query = """SELECT * FROM products"""

        if per_page:
            sql_query += f""" LIMIT {per_page} OFFSET {page*per_page}"""

        results = cls.db.execute(sql_query, filters).fetchall()
        results = [cls(*result) for result in results]
        if to_json:
            results = [result.to_json() for result in results]
        return results

    def __init__(
        self, product_id, product_name, product_price, product_image, category_id
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_image = product_image
        self.category_id = category_id

    def in_stock(self, store_id, order_qty):
        self.db.execute(
            """SELECT qty FROM stock WHERE product_id = ? AND store_id= ?""",
            (self.product_id, store_id),
        )
        qty = self.db.c.fetchone()[0]

        if qty is None or qty < order_qty:
            return False

        else:
            return True

    def to_json(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "product_image": self.product_image,
            "category_id": self.category_id,
        }

    def save(self):
        sql_query = (
            """UPDATE products SET product_name=?, category_id=? WHERE product_id=?"""
        )
        self.db.execute(
            sql_query, (self.product_name, self.category_id, self.product_id)
        )


class InventoryItem(Product):
    def __init__(self, product_id, product_name, category_id, qty, store_id):
        super().__init__(product_id, product_name, category_id)
        self.qty = qty
        self.store_id = store_id

    def ship(self, order: "OrderItem"):
        if order.qty < self.qty:
            self.qty -= order.qty
            self.save()
            order.shipping_status = 1
            order.save()

            return True

        else:
            raise ValueError("Not enough stock")

    def to_json(self):
        out_json = super().to_json()
        out_json["qty"] = self.qty
        return out_json

    def save(self):
        sql_query = """UPDATE stock SET qty=? WHERE product_id=? AND store_id=?"""
        self.db.execute(sql_query, (self.qty, self.product_id, self.store_id))
        self.db.conn.commit()


class OrderItem(InventoryItem):
    @classmethod
    def from_product(cls, product: Product, qty, order_id, shipping_status):
        return cls(
            product.product_id,
            product.product_name,
            product.category_id,
            qty,
            order_id,
            shipping_status,
        )

    def __init__(
        self, product_id, product_name, category_id, qty, order_id, shipping_status
    ):
        super().__init__(product_id, product_name, category_id, qty)
        self.order_id = order_id
        self.shipping_status = shipping_status

    def to_json(self):
        out_json = super().to_json()
        out_json["order_id"] = self.order_id
        out_json["shipping_status"] = self.shipping_status
        return out_json

    def save(self):
        sql_query = """UPDATE order_details SET shipping_status=? WHERE product_id=? AND order_id=?"""
        self.db.execute(
            sql_query, (self.shipping_status, self.product_id, self.order_id)
        )
        self.db.conn.commit()
