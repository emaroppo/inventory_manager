import shutil
import pandas as pd
from datetime import datetime
import csv_generator as gen
import os

def loaded(file, dest):
    dest_folder='./Done/{}/{}-{}'.format(dest,datetime.now().strftime("%d-%m-%Y_%H%M"),file)
    shutil.move(file,dest_folder)

def add_item(item, category, qty=0):
    new_item={}
    new_item['Item']=item
    new_item['Category']=category
    new_item['Qty']=qty
    return new_item


def read_order(path='order.csv'):
    inventory_df = pd.read_csv('inventory.csv')
    unfulfilled_orders=pd.read_csv('unfulfilled.csv')

    try:
        with open(path) as file:
            order_items=file.readlines()

    except FileNotFoundError:
        print('Order File Not Found. Please Enter File Path.')
        path=input('File Path:')
        with open(path) as file:
            order_items=file.readlines()

    for item in order_items:
        item = item.split(',')


        if item[0] not in list(inventory_df['Item']):
            print('Item "{}" not previously in inventory. Please Specify Category.'.format(item[0]))
            category=input('Enter Category: ')
            inventory_df=inventory_df.append(add_item(item=item[0],category=category),ignore_index=True)

        if int(inventory_df.loc[inventory_df['Item']==item[0],'Qty']) >= int(item[1]):
            inventory_df.loc[inventory_df['Item']==item[0],'Qty']-=int(item[1])
        else:
            order_qty=int(item[1])-int(inventory_df.loc[inventory_df['Item']==item[0],'Qty'])
            inventory_df.loc[inventory_df['Item']==item[0],'Qty']=0

            if item[0] not in list(unfulfilled_orders['Item']):
                unfulfilled_orders=unfulfilled_orders.append(add_item(item=item[0],category=inventory_df.loc[inventory_df['Item']==item[0],'Category'].item()), ignore_index=True)

            unfulfilled_orders.loc[unfulfilled_orders['Item'] == item[0], 'Qty'] += order_qty

    loaded(path,'Orders')
    inventory_df.to_csv('inventory.csv', index=False)
    unfulfilled_orders.to_csv('unfulfilled.csv', index=False)
    return inventory_df


def read_restock(path='restock.csv'):
    inventory_df = pd.read_csv('inventory.csv')
    unfulfilled_orders=pd.read_csv('unfulfilled.csv')

    try:
        with open(path) as file:
            restock_items = file.readlines()

    except FileNotFoundError:
        print('Restock File Not Found. Please Enter File Path.')
        path = input('File Path:')
        with open(path) as file:
            restock_items = file.readlines()

    for item in restock_items:

        item = item.split(',')

        if item[0] not in list(unfulfilled_orders['Item']) or int(unfulfilled_orders.loc[unfulfilled_orders['Item']==item[0],'Qty']==0):
            inventory_df.loc[inventory_df['Item'] == item[0], 'Qty']+=int(item[1])

        elif int(item[1])<=int(unfulfilled_orders.loc[unfulfilled_orders['Item']==item[0],'Qty']):
            unfulfilled_orders.loc[unfulfilled_orders['Item'] == item[0], 'Qty']-=int(item[1])

        else:
            restock_qty=int(item[1])-int(unfulfilled_orders.loc[unfulfilled_orders['Item'] == item[0], 'Qty'])
            unfulfilled_orders.loc[unfulfilled_orders['Item'] == item[0], 'Qty']=0
            inventory_df.loc[inventory_df['Item'] == item[0], 'Qty'] += restock_qty



        if item[0] not in list(inventory_df['Item']):
            print('Item "{}" not previously in inventory. Please Specify Category.'.format(item[0]))
            category=input('Enter Category: ')
            inventory_df=inventory_df.append(add_item(item=item[0],category=category),ignore_index=True)

        inventory_df.loc[inventory_df['Item'] == item[0], 'Qty'] += int(item[1])


    loaded(path, 'Restocks')
    inventory_df.to_csv('inventory.csv', index=False)
    unfulfilled_orders.to_csv('unfulfilled.csv', index=False)

    return inventory_df

def stock_status_mapper(qty):
    if qty>5:
        return 'In Stock'
    if qty<=5 and qty>0:
        return 'Low Stock'
    if qty==0:
        return 'Out of Stock. Check "unfulfilled.csv". '


def update_inventory():
    if not os.path.exists('order.csv') and not os.path.exists('restock.csv'):
        print('No new orders or restock found. Printing Inventory...')

    if os.path.exists('order.csv'):
        read_order()
    if os.path.exists('restock.csv'):
        read_restock()
    inventory=pd.read_csv('inventory.csv')
    inventory['Notes']=inventory['Qty'].map(stock_status_mapper)
    inventory= inventory.sort_values(by='Notes', ascending=False)
    inventory.to_csv('inventory.csv', index=False)
    return inventory

def test_function():
    gen.generate_test()
    print(update_inventory())

test_function()

