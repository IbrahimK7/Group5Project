from flask import jsonify, render_template
from flask import request, redirect
from models.CreateAccountModel import CreateAccountModel
from models.ProfileModel import ProfileModel
from models.parties import PartyModel
from pymongo import MongoClient



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

    @app.route('/settings')
    def settings_page():
        return render_template("settings.html")
    
    @app.route('/api/forgot-password')
    def forgot_password():
        return jsonify({"message": "password reset link sent!"})

    
    @app.route('/host')
    def host():
        return render_template("host.html")
    
    @app.route('/search')
    def search():
        return jsonify({"message": "Search for a party!"})
    
    @app.route('/api/create-account')
    def create_account():
        return jsonify({"message": "Create an account!"})

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/api/rate')
    def rate():
        return jsonify({"message": "Rate your experience!"})

    @app.route('/editprofile')
    def edit_profile():
        return render_template('editprofile.html')

    @app.route('/playerprofiles')
    def player_profiles():
        return render_template('playerprofiles.html')
    
    @app.route('/joinparty')
    def joinparty_page():
        game = request.args.get("game")  # e.g. Valorant

        if game:
            parties = list(party_model.collection.find({"game": game}))
        else:
            parties = list(party_model.collection.find())

        return render_template("joinparty.html", parties=parties, selected_game=game)



    @app.route('/leaveparty')
    def leaveparty_page():
        return render_template('Leaveparty.html')

    from bson import ObjectId

    @app.route('/api/update-profile', methods=['POST'])
    def update_profile():
    # TEMP: simulate logged-in user
        current_username = "marin"

        new_username = request.form.get('username')
        bio = request.form.get('bio')

        update_data = {}

        if new_username:
            update_data["username"] = new_username

        if bio is not None:
            update_data["bio"] = bio

        if update_data:
            db.Users.update_one(
                {"username": current_username},
                {"$set": update_data}
            )

        return redirect('/home')


    
    @app.route('/api/join-party', methods=['POST'])
    def join_party():
        db.player_stats.update_one(
            {"user_id": "test_user"},
            {"$set": {"party": "party_1"}},
            upsert=True
        )
        return redirect('/playerprofiles')

    

    


