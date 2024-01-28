from bson import json_util
from Models.users import UserModel
from werkzeug.security import check_password_hash
import json
import re


def pymodel_to_json(data):
    data = json.loads(json_util.dumps(data))
    if data:
        data['_id'] = data['_id']['$oid']

        return data

    return None

def check_email(email):
    regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Removing all spaces
    # email = re.sub(r"\s+", "", email, flags=re.UNICODE).lower()
    # Removing spaces at the beginning and at the end
    email = re.sub(r"^\s+|\s+$", "", email, flags=re.UNICODE).lower()
    if re.search(regex, email):
        return email
    return False

def authenticate(email, password):
    obj_user = UserModel.find_by_email(email)
    if obj_user and check_password_hash(obj_user.get('password'), password):
        return obj_user
