from flask import jsonify

def register_routes(app):
    @app.route('/api/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    @app.route('/api/login')
    def login ():
        return jsonify({"message": "you have logged in!"})