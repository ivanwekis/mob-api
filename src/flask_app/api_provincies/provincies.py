from flask import request, jsonify, Blueprint, Response, render_template
from werkzeug.security import generate_password_hash
from classes.auth import create_key
from pymongo import MongoClient
from datetime import datetime
from bson import json_util
from flask_app import mail
from flask_mail import Message

provincies = Blueprint("provincies", __name__)
MONGO_URI = "mongodb://localhost"
client = MongoClient(MONGO_URI)
db = client["weatherdata"]


@provincies.route("/api.download/<date>/<station>", methods=["POST"])
def downloadDataProvincie(date, station):
    email = request.json["email"]
    key = request.json["key"]
    user = db.users.find_one({"email": email, "key": key})
    if not user is None:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            collection = db.get_collection(date)
            information = collection.find({"Provincia": station})
            response = json_util.dumps(information)
            return Response(response, mimetype="application/json")
        except ValueError:
            return jsonify(
                {"response": "Incorrect date format. example:'/2022-12-12' "}
            )
    else:
        return jsonify({"response": "The email or key are incorrect."})


@provincies.route("/api.download/<date>", methods=["POST"])
def downloadData(date):
    email = request.json["email"]
    key = request.json["key"]
    user = db.users.find_one({"email": email, "key": key})
    if not user is None:
        try:
            print("User: {} is correct.".format(email))
            datetime.strptime(date, "%Y-%m-%d")
            collection = db.get_collection(date)
            information = collection.find()
            response = json_util.dumps(information)
            return Response(response, mimetype="application/json")
        except ValueError:
            return jsonify(
                {"response": "Incorrect date format. example:'/2022-12-12' "}
            )
    else:
        return jsonify({"response": "The email or key are incorrect."})


@provincies.route("/new-user", methods=["POST"])
def newUser():
    email = request.json["email"]
    password = request.json["password"]

    if email and password:
        user = db.users.find_one({"email": email})
        print(user)
        if user is None:
            hased_password = generate_password_hash(password)
            secret_key = create_key()
            query = {"email": email, "password": hased_password, "key": secret_key}
            id = db.users.insert_one(query)
            return jsonify(
                {
                    "_id": str(id),
                    "key": secret_key,
                    "response": "The user has been created succesfully",
                }
            )

        return jsonify({"response": "The users alredy exists"})

    return jsonify({"response": "The email or password are empty."})


@provincies.route("/new-key", methods=["POST"])
def newKey():
    username = request.json["username"]
    password = request.json["password"]

    if username and password:
        hased_password = generate_password_hash(password)
        query = {"username": username, "password": hased_password}
        new_values = {"$set": {"key": secret_key}}

        user = db.users.find_one(query)
        if user:
            secret_key = create_key()
            id = db.users.update_one(query, new_values)
            return jsonify(
                {"Update": id, "response": "The new key was update", "key": secret_key}
            )
        else:
            return jsonify({"response": "The username or email not are corrects"})
    else:
        return jsonify({"response": "Please, introduce your username and password"})


@provincies.route("/new-password/<email>", methods=["GET"])
def newPassword(email):
    password_link = create_key()
    msg = Message("Recover your password",
                sender="flaskapp.pruebas@gmail.com",
                recipients=[email])
    route = "127.0.0.1:5000/new-password-link/"+password_link
    msg.body = "To recover your password, please, use these link." + route
    print("Aquí llega")
    mail.send(msg)

    query = {"email": email}
    new_values = {"$set": {"link_password": password_link, "link_used": False}}
    id = db.users.update_one(query, new_values)
    return jsonify({"Update": str(id), "response": "The link for reset your password has been activated", "link": password_link})


@provincies.route("/new-password-link/<link>", methods=["POST"])
def recoverPassword(link):
    new_password = request.json["password"]
    if new_password:
        query = {"link_password": link, "link_used": False}
        new_values = {"$set": {"link_password": new_password, "link_used": True}}
        id = db.users.update_one(query, new_values)
        return jsonify({"Update": str(id), "response": "Your new password have been set"})
    return jsonify({"Update": str(id), "response": "Please, introduce yor new passworw in a JSON."})

