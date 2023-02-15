from db_builder import DBBuilder
from record import DBManager
from classes import Store
import argparse 
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
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode', help='user or store')
    parser.add_argument('--store_id', help='store id')
    args=parser.parse_args()
    user_type=args.mode
    store_id=args.store_id
    store=Store(store_id=store_id)


    if user_type=='user':

        print('1 - Place order')
        print('2 - Check order status')
        action = input("Select an option: ")

        if action == '1':
            store.receive_order(mode='manual')

        elif action == '2':
            order_id = input("Enter order ID: ")
            store.check_order_status(order_id)

    if user_type=='staff':

        action=''
        
        while action!='Q':
            print('1 - Orders')
            print('2 - Restocks')
            print('3 - Catalogue')
            print('(Enter Q to quit)')
            print('------------------')

            action = input("Select an option: ")

            while action != 'Q' and action != 'B':
                if action == '1':
                    print('-- Orders --')
                    print('(Enter B to go back)')
                    print('(Enter Q to quit)')
                    action=input("Select an option: ")

                elif action == '2':
                    print('-- Restocks --')
                    print('(Enter B to go back)')
                    print('(Enter Q to quit)')
                    action=input("Select an option: ")

                elif action == '3':
                    print('-- Catalogue --')
                    print('1 - Add new product')
                    print('2 - Add new category')
                    print('(Enter B to go back)')
                    print('(Enter Q to quit)')

                    action = input("Select an option: ")
                    if action == '1':
                        store.add_product()
                    elif action == '2':
                        store.add_category()
                