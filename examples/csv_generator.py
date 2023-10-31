import random
from backend.classes.db import db

def generate_csv(csv_type, length): #type=order or restock

    items_list=db.execute('SELECT product_id FROM products').fetchall()
    items_list=[i[0] for i in items_list]
    
    order_items=random.sample(items_list, length)
    order_items=[(i,random.randint(1,15)) for i in order_items]

    filename='examples/{}.csv'.format(csv_type)

    items_set = set()

    while len(items_set) < length:
        items_set.add(random.randint(0, len(items_list)-1))

    items_set=[items_list[i] for i in list(items_set)]


    with open(filename, 'w+') as file:

        for i in items_set:
            string='{},{}\n'.format(i,random.randint(1,15))
            file.write(string)

generate_csv('order', 10)