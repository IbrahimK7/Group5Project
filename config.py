from flask import Flask

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'your_secret_key_here'  # Replace with a strong secret key
    JSONIFY_PRETTYPRINT_REGULAR = True  # Optional: for pretty JSON responses