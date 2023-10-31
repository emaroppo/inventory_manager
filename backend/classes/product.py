from .db import db

class Product:
    
    db = db
    
    @classmethod
    def from_id(cls, product_id):
        args=cls.db.execute("""SELECT * FROM products WHERE product_id=?""", (product_id,)).fetchone()
        product=cls(*args)
        return product
    
    @classmethod
    def add(cls ,product_name, category_id):
        cls.db.execute("""INSERT INTO products (product_name, category_id) VALUES (?,?)""", (product_name, category_id))
        return cls.db.lastrowid
    
    def __init__(self, product_id, product_name, category_id):
        
        self.product_id = product_id
        self.product_name = product_name
        self.category_id = category_id


    def in_stock(
        self, store_id, order_qty
    ):
        self.db.c.execute(
            """SELECT qty FROM stock WHERE product_id = ? AND store_id= ?""",
            (self.product_id, store_id),
        )
        qty = self.db.c.fetchone()[0]

        if qty is None or qty < order_qty:
            return False

        else:
            return True

    