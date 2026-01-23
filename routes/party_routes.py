from flask import jsonify, render_template
from models.parties import PartyModel

# Create a single instance of the PartyModel
# This handles database access for party-related data
party_model = PartyModel()


def register_party_routes(app):
    """
    Register party-related routes on the Flask application.

    This includes:
    - an HTML page to view and join parties
    - an API endpoint to retrieve parties as JSON
    """

    # -------------------- PARTIES PAGE --------------------
    @app.route("/parties")
    def parties_page():
        """
        Render the parties page (joinparty.html).
        """
        # Retrieve all party documents from the database
        parties = list(party_model.collection.find())

        # Convert MongoDB ObjectId to string for template compatibility
        for p in parties:
            p["_id"] = str(p["_id"])

        # Render the page and inject parties into the template context
        return render_template("joinparty.html", parties=parties)

    # -------------------- PARTIES API --------------------
    @app.route("/api/parties")
    def api_parties():
        """
        Return all parties as JSON.
        """
        # Retrieve all party documents from the database
        parties = list(party_model.collection.find())

        # Convert ObjectId to string so the data is JSON-serializable
        for p in parties:
            p["_id"] = str(p["_id"])

        # Return the party list as JSON
        return jsonify(parties)
