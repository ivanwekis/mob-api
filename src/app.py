from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from classes.auth import create_key

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/weatherdata"
mongo = PyMongo(app)


@app.route("/api.download", methods=["GET"])
def download_data():
    return "Mensaje recibido"


@app.route("/new_user", methods=["POST"])
def new_user():
    email = request.json["email"]
    password = request.json["password"]
    
    if email and password:
        user = mongo.db.users.find_one({"email": email})
        print(user)
        if  user is None :
            hased_password = generate_password_hash (password)
            secret_key = create_key()
            id = mongo.db.users.insert_one({"email": email, "password": hased_password, "key": secret_key})
            return jsonify({"_id": str(id), "key": secret_key, "response": "The user has been created succesfully"})

        return jsonify({"response": "The users alredy exists"})

    return jsonify({"response": "The email or password are empty."})

    

if __name__ == "__main__":
    app.run(debug=True, port=5000)