from flask import jsonify, render_template
from flask import request, redirect
from flask import session
from models.CreateAccountModel import CreateAccountModel
from models.parties import PartyModel
from models.login_model import LoginModel
from pymongo import MongoClient
from datetime import datetime


from .home import register_home_routes
from .auth import register_auth_routes
from .inbox_routes import register_inbox_routes
from .party_routes import register_party_routes


import os


party_model = PartyModel()
create_account_model = CreateAccountModel()
login_model = LoginModel()
# profile_model = ProfileModel()


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
        return render_template("Search.html")

    @app.route('/rate')
    def rate_page():
        return render_template("Rate.html")

    @app.route('/api/create-account')
    def create_account():
        return jsonify({"message": "Create an account!"})

    @app.route('/api/rate')
    def rate():
        return jsonify({"message": "Rate your experience!"})

    @app.route('/editprofile')
    def edit_profile():
        current_user_id = session.get("user_id")
        if not current_user_id:
            return redirect('/login')
        
        user = login_model.get_user_by_id(current_user_id)
        if not user:
            return redirect('/home')
        
        return render_template('editprofile.html', current_username=user.get('username', ''), current_bio=user.get('bio', ''))

    @app.route('/playerprofiles')
    def player_profiles():
        game = request.args.get('game')
        return render_template('playerprofiles.html', selected_game=game)

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
        current_user_id = session.get("user_id")
        if not current_user_id:
            return redirect('/login')  # or handle not logged in

        new_username = request.form.get('username')
        bio = request.form.get('bio')
        delete_user = request.form.get('delete_user')
        update_data = {}

        if new_username:
            update_data["username"] = new_username

        if bio is not None:
            update_data["bio"] = bio

        if delete_user == 'on':
            login_model.collection.delete_one({"_id": ObjectId(current_user_id)})
            session.clear()
            return redirect('/login') 
        
        

        if update_data:
            login_model.collection.update_one(
                {"_id": ObjectId(current_user_id)},
                {"$set": update_data}
            )
            # Insert into editedprofiles collection
            edit_data = {
                "user_id": ObjectId(current_user_id),
                "username": session.get("username"),
                "changes": update_data,
                "timestamp": datetime.utcnow()
            }
            login_model.db["editedprofiles"].insert_one(edit_data)
            # Optionally update session username if changed
            if new_username:
                session["username"] = new_username

        return redirect('/home')

    @app.route('/api/send-message', methods=['POST'])
    def send_message():
        current_user_id = session.get("user_id")
        if not current_user_id:
            return redirect('/login')

        message = request.form.get('message')
        if message:
            msg_data = {
                "user_id": ObjectId(current_user_id),
                "message": message,
                "timestamp": datetime.utcnow()
            }
            login_model.db["player profiles msg"].insert_one(msg_data)

        return redirect('/playerprofiles')

    @app.route('/api/leave-party', methods=['POST'])
    def leave_party():
        current_user_id = session.get("user_id")
        if not current_user_id:
            return redirect('/login')

        username = session.get("username")
        leave_data = {
            "user_id": ObjectId(current_user_id),
            "username": username,
            "timestamp": datetime.utcnow()
        }
        login_model.db["leftparties"].insert_one(leave_data)

        return redirect('/rate')

    @app.route('/api/join-party', methods=['POST'])
    def join_party():
        current_user_id = session.get("user_id")
        if not current_user_id:
            return redirect('/login')

        party_id = request.form.get('party_id')
        if party_id:
            # Fetch the party to get the game
            party = party_model.collection.find_one(
                {"_id": ObjectId(party_id)})
            if party:
                game = party.get('game', 'Unknown')
                join_data = {
                    "user_id": ObjectId(current_user_id),
                    "party_id": ObjectId(party_id),
                    "timestamp": datetime.utcnow()
                }
                login_model.db["joined parties"].insert_one(join_data)
                return redirect(f'/playerprofiles?game={game}')
            else:
                return redirect('/joinparty')  # Party not found

        return redirect('/joinparty')
