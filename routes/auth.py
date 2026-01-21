from flask import render_template, request, redirect, url_for
from models.login_model import LoginModel

login_model = LoginModel()

def register_auth_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = login_model.authenticate(email, password)

            if user:
                return redirect('/home')
            else:
                return render_template("login.html", error="Invalid email or password")

        return render_template("login.html")


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

            if not username or not email or not password:
                return render_template("createaccount.html", error="Please fill in all fields.")

            # Optional but strongly recommended: avoid duplicates
            existing = login_model.collection.find_one({
                "$or": [{"email": email}, {"username": username}]
            })
            if existing:
                return render_template("createaccount.html", error="Username or email already exists.")

            user_data = {
                "username": username,
                "email": email,
                "password": password
            }

            login_model.create_user(user_data)
            return redirect(url_for("login"))

        return render_template("createaccount.html")
