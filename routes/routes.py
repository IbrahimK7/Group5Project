from flask import jsonify, render_template
import os

def register_routes(app):
    @app.route('/api/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    @app.route('/login')
    def login ():
        return render_template("login.html")
        # return jsonify({"message": "you have logged in!"})
    
    @app.route('/api/forgot-password')
    def forgot_password():
        return jsonify({"message": "password reset link sent!"})
    
    @app.route('/api/home')
    def home():
        return jsonify({"message": "Welcome to the home page!"})
    
    @app.route('/api/inbox')
    def inbox():
        return jsonify({"message": "Here is your inbox!"})
    
    @app.route('/api/host')
    def host():
        return jsonify({"message": "Host a party!"})
    
    @app.route('/api/search')
    def search():
        return jsonify({"message": "Search for a party!"})
    
    @app.route('/api/settings')
    def settings():
        return jsonify({"message": "User settings page!"})
    
    @app.route('/api/create-account')
    def create_account():
        return jsonify({"message": "Create an account!"})

    @app.route('/api/profile')
    def profile():
        return jsonify({"message": "This is your profile!"})

    @app.route('/api/rate')
    def rate():
        return jsonify({"message": "Rate your experience!"})
