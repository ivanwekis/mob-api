from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from classes.auth import create_key
from pymongo import MongoClient


provincies = Blueprint('provincies',__name__)
MONGO_URI = "mongodb://localhost"
client = MongoClient(MONGO_URI)
db = client["weatherdata"]

@provincies.route("/test", methods=["GET"])
def test():
    return "mensaje recibido"


@provincies.route("/api.download/<email>/<key>", methods=["POST"])
def download_data(email, key):

    return "Mensaje recibido"


@provincies.route("/new_user", methods=["POST"])
def new_user():
    email = request.json["email"]
    password = request.json["password"]
    
    if email and password:
        user = db.users.find_one({"email": email})
        print(user)
        if  user is None :
            hased_password = generate_password_hash (password)
            secret_key = create_key()
            id = db.users.insert_one({"email": email, "password": hased_password, "key": secret_key})
            return jsonify({"_id": str(id), "key": secret_key, "response": "The user has been created succesfully"})

        return jsonify({"response": "The users alredy exists"})

    return jsonify({"response": "The email or password are empty."})