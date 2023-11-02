from .db import db, conn


class Category:
    db = db
    conn = conn

    @classmethod
    def from_id(cls, category_id):
        args = cls.db.execute(
            """SELECT * FROM categories WHERE category_id=?""", (id, category_id)
        ).fetchone()
        category = cls(*args)
        return category

    @classmethod
    def add(cls, category_name):
        db.execute(
            """INSERT INTO categories (category_name) VALUES (?)""", (category_name,)
        )
        conn.commit()
        return cls(cls.db.lastrowid, category_name)

    @classmethod
    def search(cls, to_json=False):
        results = cls.db.execute("""SELECT * FROM categories""").fetchall()
        results = [cls(*result) for result in results]
        if to_json:
            results = [result.to_json() for result in results]
        return results

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

    def to_json(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }
