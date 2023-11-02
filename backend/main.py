from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from classes.product import Product
from classes.category import Category
from classes.store import Store
from classes.order import CustomerOrder
from classes.cart import Cart
from classes.db import db
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv("../.env")
origins = os.getenv("ALLOWED_ORIGINS").split(",")


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
    return Product.from_id(product_id, to_json=True)


@app.get("/products/add_product")
async def add_product(product_name, category_id):
    product = Product.add(product_name, category_id)
    return product.to_json()


@app.get("/categories")
async def show_categories():
    return Category.search(to_json=True)


@app.post("/categories/add_category")
async def add_category(request: Request):
    category_name = await request.json()
    category_name = category_name["category_name"]
    category = Category.add(category_name)
    return category.to_json()


@app.get("/stores")
async def show_stores():
    return Store.search(to_json=True)


@app.get("/stores/find")
async def find_stores(zip_query):
    stores = Store.search(zip_query, to_json=True)
    print(stores)
    return stores


@app.get("/stores/{store_id}")
async def show_store(store_id):
    return Store.from_id(store_id, to_json=True)


@app.get("/stores/add_store")
async def add_store(street_n, street_name, city, ZIP, store_image):
    store = Store.add(street_n, street_name, city, ZIP, store_image)
    return store.to_json()


@app.post("/user/orders")
async def show_orders(user_id):
    return CustomerOrder.search(user_id=user_id, to_json=True)


@app.get("/user/orders/{order_id}")
async def show_order(order_id):
    return CustomerOrder.from_id(order_id, to_json=True)


@app.get("/orders/add_order")
async def add_order(store_id):
    db.execute("""INSERT INTO orders (store_id) VALUES (?)""", (store_id,))
    return db.lastrowid


@app.post("/cart/add_item")
async def add_to_cart(request: Request):
    cart = Cart.from_user_id(1)
    data = await request.json()
    product_id = data["product_id"]
    print(product_id)
    qty = data["qty"]
    cart.add_item(product_id, qty)
    cart = cart.to_json()
    print(cart)
    return cart


@app.post("/cart/remove_item")
async def add_to_cart(request: Request):
    cart = Cart.from_user_id(1)
    data = await request.json()
    product_id = data["product_id"]
    print(product_id)
    qty = data["qty"]
    cart.remove_item(product_id, qty)
    cart = cart.to_json()
    print(cart)
    return cart


@app.post("/cart/checkout")
async def checkout_cart():
    cart = Cart.from_user_id(1)
    order = cart.checkout()
    return order.to_json()


@app.get("/cart")
async def show_cart():
    cart = Cart.from_user_id(1)
    return cart.to_json()
