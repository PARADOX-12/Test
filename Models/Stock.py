from db import db
from datetime import datetime

class Stock(object):
    def __init__(self, data):
        self._id = str(data.get("_id"))
        self.stocks = int(data.get("stocks"))
        self.product_type = data.get("product_type")
        self.manufacturing_date = data.get("manufacturing_date")
        self.expdate = data.get("expdate")
        self.create_at = str(datetime.utcnow())

    def save_to_db(self):
        db.stocks.update_one(
            {"_id": self._id},
            {
                "$set": {
                    "product_type": self.product_type,
                    "expdate": self.expdate,
                    "manufacturing_date": self.manufacturing_date,
                    "created_at": self.create_at,

                },
                "$inc": {"stocks": self.stocks}
            },
            True
        )

    def update_in_db(self):
        db.stocks.update_one(
            {"_id": self._id},
            {
                "$set": {
                    "product_type": self.product_type,
                    "expdate" : self.expdate
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

    @classmethod
    def find_by_id(cls,_id):
        if db.stocks.find_one({"_id": _id}):
            return Stock(db.stocks.find_one({"_id": _id})).__dict__
        return None

    @classmethod
    def delete_by_id(cls, _id):
        if db.stocks.find_one({"_id": _id}):
            return db.stocks.delete_one({"_id": _id})
        return None