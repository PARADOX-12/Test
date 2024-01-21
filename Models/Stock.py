from bson.objectid import ObjectId
from db import db
from datetime import datetime

class Stock(object):
    def __init__(self, data):
        self._id = str(data.get("_id"))
        self.stocks = int(data.get("stocks"))
        self.product_type = data.get("product_type")
        self.date = str(datetime.utcnow())

    def save_to_db(self):
        db.stocks.update_one(
            {"product_type": self.product_type},
            {
                "$set": {
                    "date": self.date
                },
                "$inc": {"stocks": self.stocks}
            },
            True
        )

    def update_in_db(self):
        db.stocks.update_one(
            {"product_type": self.product_type},
            {
                "$set": {
                    "date": self.date
                },
                "$inc": {"stocks": self.stocks}
            },
            False
        )

    @classmethod
    def find_by_product_type(cls,product_type):
        if db.stocks.find_one({"product_type": product_type}):
            return Stock(db.stocks.find_one({"product_type": product_type})).__dict__
        return None

