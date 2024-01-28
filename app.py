from flask import Flask,request,jsonify
from flask_cors import CORS
from Resources.Stocks import stocks
from flask_jwt_extended import JWTManager, \
    create_access_token, get_jwt_identity, create_refresh_token,jwt_required
from utils import check_email, authenticate
from datetime import timedelta
from Models.users import UserModel

app = Flask(__name__)
CORS(app)
app.register_blueprint(stocks)
app.config['JWT_SECRET'] = 'secret'
app.config['JWT_ALGORITHM'] = 'HS256'
ACCESS_EXPIRES = timedelta(hours=24)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.secret_key = 'super_secret'
app.config['JWT_SECRET_KEY'] = 'super-jwt-hd-secret'
jwt = JWTManager(app)


@app.route('/register', methods= ['POST'])
def register():
    try:
        body = request.get_json()

        if not body:
            return jsonify({
                "description": "Missing DATA in request",
                "error": "Missing DATA in request",
                "status": 400
            }), 400

        email = body.get('email')
        password = body.get('password')

        if not email:
            return jsonify({
                "description": "Missing email in request",
                "error": "Error",
                "status_code": 400}), 400


        if not password:
            return jsonify({
                    "description": "Missing password in request",
                    "error": "Error",
                    "status_code": 400}), 400

        valid_email = check_email(email)
        if not valid_email:
            return jsonify({
                "description": "Not a valid email in request",
                "error": "Error",
                "status_code": 400
            }), 400

        user_exist= UserModel.find_by_email(email)
        if user_exist:
            return jsonify({
                "Message": "User already exist",
                "status_code": 403
            }), 403

        data= UserModel(body)
        data.save_to_db()
        return jsonify({
            "Message": "user created successfully",
            "status": 201
        }), 201

    except Exception as e:
        return jsonify({
            "Message": str(e),
            "Status": 500
        }), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()

        if not body:
            return jsonify({
                "description": "Missing DATA in request",
                "error": "Missing DATA in request",
                "status": 400
            }), 400

        email = body.get('email')
        password = body.get('password')

        if not email:
            return jsonify({
                "description": "Missing email in request",
                "error": "Error",
                "status_code": 400}), 400

        if not password:
            return jsonify({
                "description": "Missing password in request",
                "error": "Error",
                "status_code": 400}), 400

        valid_email = check_email(email)
        if not valid_email:
            return jsonify({
                "description": "Not a valid email in request",
                "error": "Error",
                "status_code": 400}), 400
        user = authenticate(email,password)
        if not user:
            return jsonify({"description": "username or password incorrect.",
                            "error": "Error",
                            "status_code": 401}), 401  # 401

        access_token = create_access_token(identity= str(user.get("_id")))
        refresh_token = create_refresh_token(str(user.get("_id")))
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'status_code': 200
        })

    except Exception as e:
        return jsonify({
            "Message": str(e),
            "Status": 500
        }), 500


@app.route('/refresh_token', methods=["POST"])
@jwt_required(refresh= True)
def refresh_token():
   try:
       current_user = get_jwt_identity()
       if current_user:
           access_token = create_access_token(identity=current_user)
           return jsonify({
               "access_token": access_token
           }), 200

       return jsonify({
           "Message" : "Invalid credentials"
       }),401

   except Exception as e:
       return jsonify({
           "ERROR" : "error occured",
           "Message" : str(e)
       }), 500


@app.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    try:
        data= get_jwt_identity()
        user_data= UserModel.find_by_id(data)
        if user_data:
            return jsonify({
                "Message": "User deleted successfully",
                "status": 200
            }), 200

        return jsonify({
            "Message": "Error occured",
            "status": 400
        }), 401

    except Exception as e:
        return jsonify({
            "ERROR": "error occured",
            "Message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=4020)