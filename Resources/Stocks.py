from flask import jsonify,request,Blueprint
from flask_jwt_extended import jwt_required
from Models.Stock import Stock

Decrement = 'decrement'
Increment = 'increment'

stocks = Blueprint("stocks",__name__)


@stocks.route('/stockapi/stocks', methods=['POST'])
@jwt_required()
def add_stocks():
    try:
        body = request.get_json()

        if not body:
            return jsonify({
                "description": "Missing DATA in request",
                "error": "Missing DATA in request",
                "status": 400
            }), 400
        
        _id = body.get("_id")
        type= body.get("type")
        stocks= body.get("stocks")
        product_type= body.get("product_type")

        if not _id:
            return jsonify({
                "description": "Missing _id",
                "error": "Missing _id",
                "status": 400
            }), 400

        check_id = Stock.find_by_id(_id)

        if check_id:
            if type == Increment and stocks > 0:
                return jsonify({
                    "Message": "Increment cannot be performed with the same id",
                    "status": 403
                }), 403

        if not type:
            return jsonify({
                "description": "Missing type",
                "error": "Missing type",
                "status": 400
            }), 400

        check_stock = Stock.find_by_id(_id)

        if not check_stock:
            if type == Decrement and stocks < 0:
                return jsonify({
                    "description": "No data found for Decrement",
                    "error": "No data found for Decrement",
                    "status": 403
                }), 403

        if not stocks:
            return jsonify({
                "description": "Missing stocks",
                "error": "Missing stocks",
                "status": 400
            }), 400

        if type == Increment and stocks > 0:
            del body['type']
            data = Stock(body)
            data.save_to_db()
            return jsonify({"Message": "Incremented successfully",
                            "status": 201
                            }), 201

        elif type == Decrement and stocks < 0:
            decr_data = Stock(body)
            decr_data.update_in_db()
            data = Stock.find_by_id(_id)
            if data.get("stocks") <= 0:
                Stock.delete_by_id(data.get("_id"))

            return jsonify({"Message": "Decremented successfully",
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
@jwt_required()
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
