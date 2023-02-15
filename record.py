import sqlite3
import csv

class DBManager:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def add_store(self, street_n, street_name, city, zip):
        self.c.execute(
            "INSERT INTO stores (street_n, street_name, city, ZIP) VALUES (?, ?, ?, ?)",
            (street_n, street_name, city, zip),
        )
        self.conn.commit()
        return self.c.lastrowid

    def get_store_id(self, street_n, street_name, city, zip):
        self.c.execute(
            "SELECT store_id FROM stores WHERE street_n = ? AND street_name = ? AND city = ? AND ZIP = ?",
            (street_n, street_name, city, zip),
        )
        return self.c.fetchone()[0]

    def get_store_address(self, store_id):
        self.c.execute(
            "SELECT street_n, street_name, city, ZIP FROM stores WHERE store_id = ?",
            (store_id,),
        )
        return self.c.fetchone()

    def add_product(self, product_name, category_id):
        self.c.execute(
            "INSERT INTO products (product_name, category_id) VALUES (?, ?)",
            (product_name, category_id),
        )
        self.conn.commit()
        return self.c.lastrowid

    def get_product_id(self, product_name):
        self.c.execute(
            "SELECT product_id FROM products WHERE product_name = ?", (product_name,)
        )
        return self.c.fetchone()[0]

    def get_product_info(self, product_id):
        self.c.execute(
            "SELECT product_name, category_id FROM products WHERE product_id = ?", (product_id,)
        )
        return self.c.fetchone()

    def add_category(self, category_name):
        self.c.execute(
            "INSERT INTO categories (category_name) VALUES (?)", (category_name,)
        )
        self.conn.commit()
        return self.c.lastrowid

    def get_category_id(self, category_name):
        self.c.execute(
            "SELECT category_id FROM categories WHERE category_name = ?",
            (category_name,),
        )
        return self.c.fetchone()[0]

    def get_category_name(self, category_id):
        self.c.execute(
            "SELECT category_name FROM categories WHERE category_id = ?",
            (category_id,),
        )
        return self.c.fetchone()[0]
    
    def get_categories(self):
        self.c.execute("SELECT category_id, category_name FROM categories")
        return self.c.fetchall()
    
    def add_status(self, status_id, status):
        self.c.execute(
            """INSERT OR IGNORE INTO status(status_id,status)
            VALUES (?,?)""",
            (status_id, status),
        )
        self.conn.commit()
    
    def add_purchase(self, store_id, items):
        self.c.execute("""INSERT INTO orders(store_id)
        VALUES (?)""", (store_id,))
        order_id = self.c.lastrowid
        for item in items:
            self.c.execute("""INSERT INTO order_details(order_id, product_id, qty, in_stock)
            VALUES (?,?,?,?)""", (order_id, item[0].product_id, item[1], item[0].in_stock(store_id, item[1])))
        self.conn.commit()
        return order_id
    
    def retrieve_order(self, order_id):
        self.c.execute("""SELECT store_id, status_id FROM orders WHERE order_id = ?""", (order_id,))
        store_id, status_id = self.c.fetchone()
        #add retrieve status
        self.c.execute("""SELECT product_id, qty, shipped FROM order_details WHERE order_id = ?""", (order_id,))
        items = self.c.fetchall()
        return (store_id, status_id), items
        
    def ship_item(self, order_id, store_id, product_id, qty):
        try:
            #remove item from stock
            self.c.execute("""UPDATE stock SET qty = qty - ? WHERE product_id = ? AND store_id = ?""", (qty, product_id, store_id))
        except sqlite3.IntegrityError:
            print("Not enough items in stock")
        
        #mark item as shipped
        self.c.execute("""UPDATE order_details SET shipped = 1 WHERE order_id = ? AND product_id = ?""", (order_id, product_id))
        self.conn.commit()
            
    
    def update_order_status(self, order_id):
        #if all items are shipped, update order status to order_id=2
        self.c.execute("""SELECT shipped FROM order_details WHERE order_id = ?""", (order_id,))
        shipped = self.c.fetchall()
        if all(shipped):
            self.c.execute("""UPDATE orders SET status_id = 2 WHERE order_id = ?""", (order_id,))
            self.conn.commit()
        #if some items are shipped, update order status to order_id=1
        elif any(shipped):
            self.c.execute("""UPDATE orders SET status_id = 1 WHERE order_id = ?""", (order_id,))
            self.conn.commit()

        #if no items are shipped, update order status to order_id=0

        else :
            self.c.execute("""UPDATE orders SET status_id = 0 WHERE order_id = ?""", (order_id,))
            self.conn.commit()
    
    def add_restock(self, store_id, items):
        self.c.execute("""INSERT INTO restock_orders(store_id)
        VALUES (?)""", (store_id,))
        restock_id = self.c.lastrowid
        for item in items:
            self.c.execute("""INSERT INTO restock_order_details(restock_order_id, product_id, qty)
            VALUES (?,?,?)""", (restock_id, item[0].product_id, item[1]))
        return restock_id
    
    def receive_restock(self, restock_id, store_id, product_id, qty):
        
        #update stock
        self.c.execute("""INSERT INTO stock(store_id, product_id, qty)
        VALUES (?,?,?) ON CONFLICT(store_id, product_id) DO UPDATE SET qty = qty + ?""", (store_id, product_id, qty, qty))
        #mark item as received
        self.c.execute("""UPDATE restock_order_details SET received = 1 WHERE restock_order_id = ? AND product_id = ?""", (restock_id, product_id))


        self.conn.commit()
    
    def update_restock_status(self, restock_id):
        #if all items are received, update restock status to restock_id=2
        self.c.execute("""SELECT received FROM restock_order_details WHERE restock_order_id = ?""", (restock_id,))
        received = self.c.fetchall()
        if all(received):
            self.c.execute("""UPDATE restock_orders SET status_id = 2 WHERE restock_order_id = ?""", (restock_id,))
            self.conn.commit()
        #if some items are received, update restock status to restock_id=1
        elif any(received):
            self.c.execute("""UPDATE restock_orders SET status_id = 1 WHERE restock_order_id = ?""", (restock_id,))
            self.conn.commit()

        #if no items are received, update restock status to restock_id=0
        
        else :
            self.c.execute("""UPDATE restocks SET status_id = 0 WHERE restock_order_id = ?""", (restock_id,))
            self.conn.commit()


    def show_categories(self):
        self.c.execute("""SELECT * FROM categories""")
        categories = self.c.fetchall()
        return categories
            

    def show_catalog(self, store_id):
        self.c.execute("""SELECT products.product_id, products.product_name, stock.qty, products.category_id 
        FROM products LEFT JOIN stock ON stock.product_id = products.product_id WHERE store_id = ?""", (store_id,))
        catalog = self.c.fetchall()
        return catalog
    
    def show_store_inventory(self, store_id):
        self.c.execute("""SELECT product_id, qty FROM stock WHERE store_id = ?""", (store_id,))
        inventory = self.c.fetchall()
        return inventory


    
    def fill_example_db(self, stores_csv='examples/stores.csv', products_csv='examples/products.csv', categories_csv='examples/categories.csv', statuses_csv='examples/statuses.csv'):
        
        with open(stores_csv, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                street_n, street_name, city, zip= row[0], row[1], row[2], row[3]
                self.add_store(street_n, street_name, city, zip)

        with open(categories_csv, "r") as f:
            categories = f.read().splitlines()
            for category in categories:
                self.add_category(category)
        
        with open(products_csv, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                product_name, category_name = row[0], row[1]
                category_id = self.get_category_id(category_name)
                self.add_product(product_name, category_id)
        
        with open(statuses_csv, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                status_id, status = row[0], row[1]
                self.add_status(status_id, status)

    def __del__(self):
        self.conn.close()