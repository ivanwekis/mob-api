from flask import request, jsonify, Blueprint, Response
from werkzeug.security import generate_password_hash
from classes.auth import create_key
from pymongo import MongoClient
from datetime import datetime
from bson import json_util

provincies = Blueprint('provincies',__name__)
MONGO_URI = "mongodb://localhost"
client = MongoClient(MONGO_URI)
db = client["weatherdata"]


@provincies.route("/api.download/<date>/<provincie>", methods=["POST"])
def download_data_provincie(date,provincie):
    email = request.json["email"]
    key = request.json["key"]
    user = db.users.find_one({"email":email,"key":key})
    if not user is None: 
        try:
            datetime.strptime(date,"%Y-%m-%d")
            collection = db.get_collection(date)
            information = collection.find({"Provincia": provincie})
            response  = json_util.dumps(information)
            return Response(response, mimetype="application/json")
        except ValueError:
            return jsonify({"response": "Incorrect date format. example:'/2022-12-12' "}) 
    else: 
        return jsonify({"response": "The email or key are incorrect."})


@provincies.route("/api.download/<date>", methods=["POST"])
def download_data(date):
    email = request.json["email"]
    key = request.json["key"]
    user = db.users.find_one({"email":email,"key":key})
    if not user is None: 
        try:
            print("User: {} is correct." .format(email))
            datetime.strptime(date,"%Y-%m-%d")
            collection = db.get_collection(date)
            information = collection.find()
            response  = json_util.dumps(information)
            return Response(response, mimetype="application/json")
        except ValueError:
            return jsonify({"response": "Incorrect date format. example:'/2022-12-12' "}) 
    else: 
        return jsonify({"response": "The email or key are incorrect."})


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