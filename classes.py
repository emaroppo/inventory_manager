import csv
from record import DBManager

class Product:
    def __init__(self, product_id=None):
        
        self.db = DBManager()
        self.product_id = product_id
        self.product_name, self.category_id = self.db.get_product_info(product_id)


    def in_stock(
        self, store_id, order_qty
    ):
        self.db.c.execute(
            """SELECT qty FROM stock WHERE product_id = ? AND store_id= ?""",
            (self.product_id, store_id),
        )
        qty = self.c.fetchone()

        if qty is None or qty < order_qty:
            return False

        else:
            return True
        
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.db = DBManager()
    
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

class Store:
    def __init__(self, store_id):
        
        self.db = DBManager()
        self.store_id = store_id
        self.street_n, self.street_name, self.city, self.ZIP = self.db.get_store_address(store_id)

    def receive_order(self, order):
        order_id = self.db.add_purchase(self.store_id, order)
        return order_id

    def fulfill_order(self, order_id):
        order = Purchase(order_id=order_id)

        if not order.shippable_items:
            print("No items available for order")
        
        elif len(order.available_items) == len(order.items) or order.partial:
            for item in order.shippable_items:
                self.db.ship_item(order_id=order.order_id, product_id=item[0].product_id)
            self.db.update_order_status(order_id=order.order_id)

        else:
            print("Not enough items available for order")
            return
    

    def place_restock_order(self, items):
        restock_id = self.db.add_restock(self.store_id, items)
        return restock_id

    def receive_restock(self, items, restock_id):
        for item in items:
            self.db.receive_restock(restock_id, self.store_id, item[0].product_id, item[1])
            self.db.add_stock(self.store_id, item[0].product_id, item[1])
        self.db.update_restock_status(restock_id=restock_id)
    
 
    def confirm_receipt(self, order_id, item_id):
        order = Purchase(order_id=order_id)
        order = self.db.get_order(order)
        order.status = "received"
        self.db.update_order(order)

class Customer:
    def __init__(self) -> None:
        self.db = DBManager()
        self.customer_id = None
    
    def place_order(self, store_id, items):
        items = [(Product(product_id=i[0]), i[1]) for i in items]
        return store_id, items
        
