from db_builder import DBBuilder
from record import DBManager
from classes import Store
import sys
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
#run app from command line
if __name__=='__main__':
    user_type=sys.argv[1]
    if user_type=='user':
        store_id=sys.argv[2]
        store=Store(store_id=store_id)
        store.receive_order(mode='manual')

