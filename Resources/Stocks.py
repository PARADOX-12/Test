from flask import jsonify,request,Blueprint
from Models.Stock import Stock

Decrement = 'decrement'
Increment = 'increment'
MAX_REQ_SIZE = 20

stocks = Blueprint("stocks",__name__)


@stocks.route('/stockapi/stocks', methods=['POST'])
def add_stocks():
    try:
        body = request.get_json()

        if not body:
            return jsonify({
                "description": "Missing DATA in request",
                "error": "Missing DATA in request",
                "status": 400
            }), 400

        type= body.get("type")
        stocks= body.get("stocks")
        product_type= body.get("product_type")

        if not type:
            return jsonify({
                "description": "Missing type",
                "error": "Missing type",
                "status": 400
            }), 400

        check_stock = Stock.find_by_product_type(product_type)

        if not check_stock:
            if type == Decrement:
                return jsonify({
                    "description": "Decrement cannot be Performed",
                    "error": "Decrement cannot be performed",
                    "status": 403
                }), 403

        if not stocks:
            return jsonify({
                "description": "Missing stocks",
                "error": "Missing stocks",
                "status": 400
            }), 400

        if type == Increment:
            del body['type']
            data = Stock(body)
            data.save_to_db()
            return jsonify({"Message": "Incremented successfully",
                            "status": 201
                            }), 201

        elif type == Decrement:
            decr_data = Stock(body)
            decr_data.update_in_db()
            return jsonify({"Message": " Decremented successfully",
                            "status": 201
                            }), 201

        return jsonify({"Message": "Error occurred ",
                        "Error" : "Error occurred ",
                        "status": 400
                        }), 400

    except Exception as e:
        return jsonify({
            "Message": str(e)
        }),500


@stocks.route('/stockapi/<string:product_type>', methods=['GET'])
def decrement_stocks(product_type):
    try:
        data = Stock.find_by_product_type(product_type)

        if data:
            return jsonify(data)

        return jsonify({
            "description": "Data not found",
            "error": "Data not found",
            "status": 404
        }), 404

    except Exception as e:
        return jsonify({
            "Message": str(e)
        }),500
