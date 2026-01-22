from flask import jsonify, render_template
from models.parties import PartyModel

party_model = PartyModel()

def register_party_routes(app):

    @app.route("/parties")
    def parties_page():
        parties = list(party_model.collection.find())
        for p in parties:
            p["_id"] = str(p["_id"])
        return render_template("joinparty.html", parties=parties)

    @app.route("/api/parties")
    def api_parties():
        parties = list(party_model.collection.find())
        for p in parties:
            p["_id"] = str(p["_id"])
        return jsonify(parties)
