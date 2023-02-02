import reader
from db_manager import Inventory, setup_db
import sqlite3
import random

def example_restock(items_number=10):
    # retrieve list of store ids fro db
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT store_id FROM stores")
    store_ids = c.fetchall()

    # retrieve list of product names from db
    c.execute("SELECT product_name FROM products")
    product_names = c.fetchall()

    # write csv file with number of rows = items_numbers lines where each row is a store_id, product_, and a random qty (between 0 and 100)
    with open("examples/restock.csv", "w") as f:
        for i in range(items_number):
            store_id = random.choice(store_ids)[0]
            product_name = random.choice(product_names)[0]
            qty = random.randint(0, 100)
            f.write(f"{store_id},{product_name},{qty}" + "\n")


inv = Inventory()
order = reader.order_from_csv("examples/restock.csv")
inv.fulfill_order(order)
