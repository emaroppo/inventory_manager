import csv
from record import DBManager
from prettytable import PrettyTable
import re

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
        qty = self.db.c.fetchone()[0]

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

    #Order

    def check_order_status(self, order_id):
        order= self.db.retrieve_order(order_id)
        order_view = PrettyTable()
        order_view.field_names = ["Order ID", "Store ID", "Status ID"]
        order_view.add_row((order_id,) + order[0])
        print(order_view)
        order_items_view = PrettyTable()
        order_items_view.field_names = ["Product ID", "Product", "Quantity", "Shipped"]
        for item in order[1]:
            order_items_view.add_row((item[0],)+(self.db.get_product_info(item[0])[0],)+(item[1], item[2]))
        print(order_items_view)

    def view_cart(self, cart):
        product_id = ''

        while product_id != 'X':
            cart_view = PrettyTable()
            cart_view.field_names = ["Product ID", "Product", "Quantity", "Available"]
            for item in cart:
                cart_view.add_row((item[0].product_id, item[0].product_name, item[1], item[0].in_stock(self.store_id, item[1])))
            print(cart_view)
            print('Enter Product ID to remove item from cart, enter "X" to close cart')
            product_id = input("Select a product: ")
            try: 
                cart = [i for i in cart if i[0].product_id != int(product_id)]
            except:
                print('Invalid input')
        
        cart= [i for i in cart if i[0] != product_id]
        return cart

    def receive_order(self, cart=[], mode='auto', items_per_page=10):
        
        input_command = ''

        
        if mode == 'manual':
            #load categories, catalog, stock
            categories = self.db.get_categories()
            catalog = self.db.show_catalog(self.store_id)
            #show categories
            
            while input_command != 'Checkout' and input_command != 'Q':
                categories_view = PrettyTable()
                categories_view.field_names = ["Category ID", "Category"]
                for category in categories:
                    categories_view.add_row(category)
                print(categories_view)
                print(''' Enter "Checkout" to finish, Enter "Q" to quit''')
                
                input_command = input("Select a category: ")

                if input_command == 'Cart':
                        self.view_cart(cart)
                        input_command = input("Select a category: ")

                try :
                    input_command = int(input_command)
                    filtered_catalog = [i for i in catalog if i[-1] == input_command]
                    catalog_pages = [filtered_catalog[i:i+items_per_page] for i in range(0, len(filtered_catalog), items_per_page)]
                    current_page = 0
                except ValueError:
                    pass
                #show product_id, products & quantity in stock for selected category
                #divide results in pages
                while input_command != 'Q' and input_command != 'Checkout' and input_command != 'C':
                    #show page
                    catalog_view = PrettyTable()
                    catalog_view.field_names = ["Product ID", "Product", "Stock"]
                    for i in catalog_pages[current_page]:  
                        catalog_view.add_row(i[:-1])
                    print(catalog_view)
                    print(f'{current_page+1}/{len(catalog_pages)}')
                    print('"P"/"N" to go to previous/next page; Enter "C" to go back to categories;') 
                    print('Enter "Checkout" to finish, Enter "Q" to quit')
                    input_command = input("Select a product: ")
                    if input_command == 'Cart':
                        self.view_cart(cart)
                    if input_command == 'P':
                        current_page -= 1
                    elif input_command == 'N':
                        current_page += 1
                    elif input_command in ('C', 'Q', 'Checkout'):
                        break
                    elif input_command in [str(i[0]) for i in catalog_pages[current_page]]:
                        product_id = int(input_command)
                        product_qty = input("Enter quantity: ")
                        try:
                            cart.append((Product(product_id=product_id), int(product_qty)))
                        except ValueError:
                            print("Invalid input")
                    else:
                        print("Invalid input")
                        input_command = ''
        if input_command !='Q':
            cart = [(Product(product_id=i[0]), i[1]) for i in cart]
            order_id = self.db.add_purchase(self.store_id, cart)
        else : 
            return
        if input_command == 'Checkout':
            print(f'Order ID: {order_id}')

        return order_id

    def fulfill_order(self, order_id):
        order = Purchase(order_id=order_id)

        if not order.shippable_items:
            print("No items available for order")
        
        elif len(order.available_items) == len(order.items) or order.partial:
            for item in order.shippable_items:
                self.db.ship_item(store_id=self.store_id, qty=item[1], order_id=order.order_id, product_id=item[0].product_id)
            self.db.update_order_status(order_id=order.order_id)

        else:
            print("Not enough items available for order")
            return
    
    #Restock
    def place_restock_order(self, items):
        restock_id = self.db.add_restock(self.store_id, items)
        return restock_id

    def receive_restock(self, items, restock_id):
        for item in items:
            self.db.receive_restock(restock_id, self.store_id, item[0].product_id, item[1])
        self.db.update_restock_status(restock_id=restock_id)
    
 
    def confirm_receipt(self, order_id, item_id):
        order = Purchase(order_id=order_id)
        order = self.db.get_order(order)
        order.status = "received"
        self.db.update_order(order)
    
    #Update Catalog
    def add_category(self, category_name=''):
        if not category_name:
            category_name = input("Enter category name: ")

        category_id=self.db.add_category(category_name)
        return category_id
    
    def add_product(self, product_name='', category_id=None):
        if not product_name:
            product_name = input("Enter product name: ")
        if not category_id:
            category= input("Enter category: ")
        print(f'Add: {product_name} ({category}), confirm? (Y/N)')
        check = input()
        if check == 'Y':
            try:
                category_id = self.db.get_category_id(category)
            except:
                category_id=self.add_category(category)
            
        self.db.add_product(product_name, category_id)
    

class Customer:
    def __init__(self) -> None:
        self.db = DBManager()
        self.customer_id = None
    
    def place_order(self, store_id, items):
        return store_id, items