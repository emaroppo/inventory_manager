from .db import db

class User:
    db = db
    def __init__(self) -> None:
        self.user_id = None
        self.username = None
        self.password = None

class Customer(User):
    db = db
    def __init__(self) -> None:
        super().__init__()
        self.customer_id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone = None
        self.address = None

    def place_order(self, store_id, items):
        return store_id, items
    
class Employee(User):
    db = db
    def __init__(self) -> None:
        super().__init__()
        self.employee_id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone = None
        self.address = None
        self.store_id = None
        self.role_id = None

    def create_order(self, store_id, items):
        return store_id, items
    
