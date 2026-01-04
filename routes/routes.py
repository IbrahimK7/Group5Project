from flask import jsonify, render_template
from flask import request, redirect
from models.CreateAccountModel import CreateAccountModel
from models.ProfileModel import ProfileModel
from models.parties import PartyModel

from .home import register_home_routes
from .auth import register_auth_routes

import os

party_model = PartyModel()
create_account_model = CreateAccountModel()
profile_model = ProfileModel()

def register_routes(app):
    register_home_routes(app)
    register_auth_routes(app)

    @app.route('/api/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    
    @app.route('/api/forgot-password')
    def forgot_password():
        return jsonify({"message": "password reset link sent!"})
    
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
