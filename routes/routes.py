from flask import jsonify, render_template
from flask import request, redirect
from models.login_model import LoginModel
import os

login_model = LoginModel()

def register_routes(app):
    @app.route('/api/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = login_model.authenticate(email, password)

            if user:
                return redirect('/home')   # success → go to home page
            else:
                return render_template("home.html", error="Invalid email or password")

        return render_template("login.html") 
    
    @app.route('/api/forgot-password')
    def forgot_password():
        return jsonify({"message": "password reset link sent!"})
    
    @app.route('/home')
    def home():
        return render_template("home.html")
    
    @app.route('/inbox')
    def inbox():
        return render_template("messages.html")
    
    @app.route('/host')
    def host():
        return render_template("host.html")
    
    @app.route('/search')
    def search():
        return jsonify({"message": "Search for a party!"})
    
    @app.route('/settings')
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
