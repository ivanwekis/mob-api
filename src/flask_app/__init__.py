from distutils.command.config import config
from flask import Flask
from flask_app.api_provincies.provincies import provincies


app = Flask(__name__)
app.register_blueprint(provincies)
app.config.from_object("config.DevelopmentConfig")