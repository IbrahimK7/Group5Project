from flask import jsonify, render_template
from flask import request, redirect
from models.CreateAccountModel import CreateAccountModel
from models.ProfileModel import ProfileModel
from models.parties import PartyModel


from .home import register_home_routes
from .auth import register_auth_routes
from .inbox_routes import register_inbox_routes
from .party_routes import register_party_routes


import os

party_model = PartyModel()
create_account_model = CreateAccountModel()
profile_model = ProfileModel()

def register_routes(app):
    register_home_routes(app)
    register_auth_routes(app)
    register_inbox_routes(app)
    register_party_routes(app)

    
    @app.route('/api/forgot-password')
    def forgot_password():
        return jsonify({"message": "password reset link sent!"})

    
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

    @app.route('/editprofile')
    def edit_profile():
        return render_template('editprofile.html')

    @app.route('/playerprofiles')
    def player_profiles():
        return render_template('playerprofiles.html')

    @app.route('/api/update-profile', methods=['POST'])
    
    def update_profile():
        username = request.form.get('username')
        bio = request.form.get('bio')

       

        result = profile_model.update_profile(username, {"bio": bio})
        

        return redirect('/home')
