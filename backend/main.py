from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from classes.product import Product
from classes.db import db

app = FastAPI()
origins = [
    "http://localhost:3000",  # adjust this to match the domain you want to allow
    # add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/products")
async def show_products(page=0, per_page=0, store_id=None, category_id=None):
    filters = []
    if store_id:
        filters.append({"store_id": store_id})
    if category_id:
        filters.append({"category_id": category_id})
    return Product.search(filters, page, per_page, to_json=True)


@app.get("/products/{product_id}")
async def show_product(product_id):
    return db.execute(
        """SELECT * FROM products WHERE product_id=?""", (product_id,)
    ).fetchone()


@app.get("/products/add_product")
async def add_product(product_name, category_id):
    db.execute(
        """INSERT INTO products (product_name, category_id) VALUES (?,?)""",
        (product_name, category_id),
    )
    return db.lastrowid


@app.get("/categories")
async def show_categories():
    return db.execute("""SELECT * FROM categories""").fetchall()


@app.get("/categories/{category_id}")
async def show_category(category_id):
    return db.execute(
        """SELECT * FROM categories WHERE category_id=?""", (category_id,)
    ).fetchone()


@app.get("/categories/add_category")
async def add_category(category_name):
    db.execute(
        """INSERT INTO categories (category_name) VALUES (?)""", (category_name,)
    )
    return db.lastrowid


@app.get("/stores")
async def show_stores():
    return db.execute("""SELECT * FROM stores""").fetchall()


@app.get("/stores/{store_id}")
async def show_store(store_id):
    return db.execute(
        """SELECT * FROM stores WHERE store_id=?""", (store_id,)
    ).fetchone()


@app.get("/stores/add_store")
async def add_store(street_n, street_name, city, ZIP):
    db.execute(
        """INSERT INTO stores (street_n, street_name, city, ZIP) VALUES (?, ?, ?, ?)""",
        (street_n, street_name, city, ZIP),
    )
    return db.lastrowid


@app.get("/orders")
async def show_orders():
    return db.execute("""SELECT * FROM orders""").fetchall()


@app.get("/orders/{order_id}")
async def show_order(order_id):
    return db.execute(
        """SELECT * FROM orders WHERE order_id=?""", (order_id,)
    ).fetchone()


@app.get("/orders/add_order")
async def add_order(store_id):
    db.execute("""INSERT INTO orders (store_id) VALUES (?)""", (store_id,))
    return db.lastrowid
