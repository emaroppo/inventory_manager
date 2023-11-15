from .db import db
class Product:
    db = db

    @classmethod
    def from_id(cls, product_id):
        print(product_id)
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
        parameters = []
        if filters:
            query_parts = []
            for filter_dict in filters:
                filter_clauses = []
                for key, value in filter_dict.items():
                    filter_clauses.append(f"{key}=?")
                    parameters.append(value)
                query_parts.append(" AND ".join(filter_clauses))
            query = "SELECT * FROM products WHERE " + " OR ".join(query_parts)
        else:
            query = "SELECT * FROM products"

        if per_page:
            query += " LIMIT ? OFFSET ?"
            parameters.extend([per_page, page * per_page])

        results = cls.db.execute(query, parameters).fetchall()
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


class InventoryItem:
    #TO DO: implement from_db method
    db = db
    def __init__(self, product:Product, qty, store_id):
        self.product=product
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
        out_json = self.product.to_json()
        out_json["qty"] = self.qty
        out_json["store_id"] = self.store_id
        return out_json

    def save(self):
        sql_query = """UPDATE stock SET qty=? WHERE product_id=? AND store_id=?"""
        self.db.execute(sql_query, (self.qty, self.product.product_id, self.store_id))
        self.db.conn.commit()


class OrderItem(InventoryItem):
    #TO DO: implement from_db method
    db = db

    @classmethod
    def from_order_id(cls, order_id):
        args = cls.db.execute(
            """SELECT * FROM order_items WHERE order_id=?""", (order_id,)
        ).fetchall()
        order_items = [cls(*arg) for arg in args]
        return order_items

    def __init__(
        self, order_id, product, qty, shipping_status=0
    ): #change to match default value in db
        if type(product) == int:
            self.product = Product.from_id(product)
        elif type(product) == Product:
            self.product = product
        else:
            raise TypeError("product must be of type Product or int")
        self.qty = qty
        self.order_id = order_id
        self.shipping_status = shipping_status

    def to_json(self):
        out_json = self.product.to_json()
        out_json["qty"] = self.qty
        out_json["order_id"] = self.order_id
        out_json["shipping_status"] = self.shipping_status
        return out_json

    def save(self):
        sql_query = """UPDATE order_details SET shipping_status=? WHERE product_id=? AND order_id=?"""
        self.db.execute(
            sql_query, (self.shipping_status, self.product.product_id, self.order_id)
        )
        self.db.conn.commit()
