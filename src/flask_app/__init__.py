from flask import Flask
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
mail = Mail()
mail.init_app(app)


from flask_app.api_provincies.provincies import provincies


app.register_blueprint(provincies)

