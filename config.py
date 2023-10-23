import os

class Config:
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FLASK JWT EXTENDED
    JWT_SECRET_KEY= os.environ.get("JWT_SECRET_KEY")
    # dont forget this is a list of options ["cookies", "headers", "json", "query_string"]
    JWT_TOKEN_LOCATION = ["headers", "json"]

    # if my code doesnt work then I should remove the last line and the comment above it
    