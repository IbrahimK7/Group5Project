from flask import render_template, request, redirect

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
                return render_template("home.html", error="Invalid email or password")

        return render_template("login.html") 
