import classes
import csv
from db_builder import DBBuilder
from record import DBManager
import os

# create example db if not there


if not os.path.isfile("inventory.db"):
    db_manager = DBManager()
    db_builder = DBBuilder()
    db_builder.set_up_tables()
    db_manager.fill_example_db()
else:
    db_manager = DBManager()

# receive restock

restock = []
with open("examples/order.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        restock.append(row)
        
    restock = [(classes.Product(product_id=i[0]), int(i[1])) for i in restock]

store_id = 1
store = classes.Store(store_id=store_id)
restock_id=store.place_restock_order(restock)
store.receive_restock(items=restock, restock_id=restock_id)


# place order

order = []
with open("examples/order.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        order.append(row)
    order = [(classes.Product(product_id=int(i[0])), int(i[1])) for i in order]

store_id = 1
store = classes.Store(store_id=store_id)
order_id=store.receive_order(order)
store.fulfill_order(order_id)
