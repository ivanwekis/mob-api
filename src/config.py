class BaseConfig():
    SECRET_KEY = "cuchi"
    DEBUG = True
    TESTING = False

class DevelopmentConfig(BaseConfig):
    TESTING = True
    