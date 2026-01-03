from flask import jsonify, render_template
from flask import request, redirect
from models.CreateAccountModel import CreateAccountModel
from models.ProfileModel import ProfileModel
from models.login_model import LoginModel
from models.parties import PartyModel
from models.whats_hot import WhatsHotModel

import os

login_model = LoginModel()
party_model = PartyModel()
whats_hot_model = WhatsHotModel()
create_account_model = CreateAccountModel()
profile_model = ProfileModel()

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
                return redirect('/home')  
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


    @app.route('/parties', methods=["GET"])
    def get_parties():
        parties = list(party_model.collection.find())

        # Convert Mongo ObjectId to string for easy usage in JSON
        for party in parties:
            party["_id"] = str(party["_id"])

        return render_template("joinparty.html")
    
    @app.route('/api/parties')
    def api_parties():
        parties = list(party_model.collection.find())
        for party in parties:
            party['_id'] = str(party['_id'])
        return jsonify(parties)
    
<<<<<<< HEAD
    @app.route('/api/whats-hot')
    def api_whats_hot():
        return jsonify(whats_hot_model.get_all_games())
=======


    @app.route("/api/whats-hot")
    def get_whats_hot():
        return jsonify(whats_hot_model.get_all_games())
>>>>>>> 2b65b3787af436b116f144dee6456414a92b15fe
