import random
import pandas as pd

inventory_df=pd.read_csv('inventory.csv', index_col='Item')
items_list=list(inventory_df.index)

def generate_csv(csv_type, length): #type=order or restock

    filename='{}.csv'.format(csv_type)

    items_set = set()

    while len(items_set) < length:
        items_set.add(random.randint(0, len(items_list)-1))

    items_set=[items_list[i] for i in list(items_set)]


    with open(filename, 'w+') as file:

        for i in items_set:
            string='{},{}\n'.format(i,random.randint(1,15))
            file.write(string)

def generate_test():
    generate_csv('order',10)
    generate_csv('restock',10)