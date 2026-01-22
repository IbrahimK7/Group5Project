from flask import render_template, request, redirect, session, url_for
from models.login_model import LoginModel

login_model = LoginModel()


def register_auth_routes(app):

    # -------------------- LOGIN --------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        # If user submits the form
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = login_model.authenticate(email, password)

            # Login successful
            if user:
                session["user_id"] = user["_id"]
                session["username"] = user.get("username")
                return redirect(url_for("home"))

            # Login failed
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # Show login page
        return render_template("login.html")

    # -------------------- REGISTER --------------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        # If user submits the form
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            # Check required fields
            if not username or not email or not password:
                return render_template(
                    "createaccount.html",
                    error="Please fill in all fields."
                )

            # Prevent duplicate username or email
            existing = login_model.get_user_by_email(email, include_password=True)
            if existing:
                return render_template(
                    "createaccount.html",
                    error="Username or email already exists."
                )

            # Create new user
            login_model.create_user({
                "username": username,
                "email": email,
                "password": password
            })

            return redirect(url_for("login"))

        # Show registration page
        return render_template("createaccount.html")

    # -------------------- LOGOUT --------------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    # -------------------- PROFILE --------------------
    @app.route("/profile")
    def profile():
        # Require login
        if "user_id" not in session:
            return redirect(url_for("login"))

        user = login_model.get_user_by_id(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))

        return render_template("profile.html", user=user)
