from backend.classes.order import CustomerOrder, OrderItem, Product


class Cart:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.items = []

    def add_item(self, product_id, qty):
        self.items.append((Product.from_id(product_id), qty))

    def checkout(self):
        # create order
        order = CustomerOrder.add(user_id=self.user_id)
        # add items to order
        order.add_items(self.items)
        return order
