from flask import jsonify

def register_routes(app):
    @app.route('/api/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    @app.route('/api/login')
    def login ():
        return jsonify({"message": "you have logged in!"})
    
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
    
