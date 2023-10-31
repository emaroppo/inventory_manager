from fastapi import FastAPI
from classes.db import db
app=FastAPI()

@app.get("/products")
async def show_products(page=0, per_page=10, store_id=None, category_id=None):
    if category_id is None and store_id is None:
        return db.execute("""SELECT * FROM products""").fetchall()
    elif category_id is None and store_id is not None:
        return db.execute("""SELECT * FROM products WHERE product_id IN (SELECT product_id FROM stock WHERE store_id=?)""", (store_id,)).fetchall()
    elif category_id is not None and store_id is None:
        return db.execute("""SELECT * FROM products WHERE category_id=?""", (category_id,)).fetchall()
    else:
        return db.execute("""SELECT * FROM products WHERE product_id IN (SELECT product_id FROM stock WHERE store_id=?) AND category_id=?""", (store_id, category_id)).fetchall()
    
@app.get("/products/{product_id}")
async def show_product(product_id):
    return db.execute("""SELECT * FROM products WHERE product_id=?""", (product_id,)).fetchone()

@app.get("/products/add_product")
async def add_product(product_name, category_id):
    db.execute("""INSERT INTO products (product_name, category_id) VALUES (?,?)""", (product_name, category_id))
    return db.lastrowid

@app.get("/categories")
async def show_categories():
    return db.execute("""SELECT * FROM categories""").fetchall()

@app.get("/categories/{category_id}")
async def show_category(category_id):
    return db.execute("""SELECT * FROM categories WHERE category_id=?""", (category_id,)).fetchone()

@app.get("/categories/add_category")
async def add_category(category_name):
    db.execute("""INSERT INTO categories (category_name) VALUES (?)""", (category_name,))
    return db.lastrowid

@app.get("/stores")
async def show_stores():
    return db.execute("""SELECT * FROM stores""").fetchall()

@app.get("/stores/{store_id}")
async def show_store(store_id):
    return db.execute("""SELECT * FROM stores WHERE store_id=?""", (store_id,)).fetchone()

@app.get("/stores/add_store")
async def add_store(street_n, street_name, city, ZIP):
    db.execute("""INSERT INTO stores (street_n, street_name, city, ZIP) VALUES (?, ?, ?, ?)""", (street_n, street_name, city, ZIP))
    return db.lastrowid

@app.get("/orders")
async def show_orders():
    return db.execute("""SELECT * FROM orders""").fetchall()

@app.get("/orders/{order_id}")
async def show_order(order_id):
    return db.execute("""SELECT * FROM orders WHERE order_id=?""", (order_id,)).fetchone()

@app.get("/orders/add_order")
async def add_order(store_id):
    db.execute("""INSERT INTO orders (store_id) VALUES (?)""", (store_id,))
    return db.lastrowid

