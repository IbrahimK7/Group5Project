from flask import render_template, request, redirect, session, url_for
from models.login_model import LoginModel

# Create a single instance of the LoginModel
# This handles user authentication and database access
login_model = LoginModel()


def register_auth_routes(app):
    """
    Register all authentication-related routes (login, register, logout, profile)
    on the given Flask application instance.
    """

    # -------------------- LOGIN --------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Handle user login.

        - GET: display the login form
        - POST: process login credentials
        """
        # If the user submits the login form
        if request.method == "POST":
            # Retrieve form data sent by the browser
            email = request.form.get("email")
            password = request.form.get("password")

            # Attempt to authenticate the user
            user = login_model.authenticate(email, password)

            # Login successful
            if user:
                # Store user information in the session
                # Session data is stored server-side (signed cookie by Flask)
                session["user_id"] = user["_id"]
                session["username"] = user.get("username")

                # Redirect user to the home page after login
                return redirect(url_for("home"))

            # Login failed: invalid credentials
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # GET request: simply display the login page
        return render_template("login.html")

    # -------------------- REGISTER --------------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        """
        Handle user registration.

        - GET: display the registration form
        - POST: validate input and create a new user
        """
        # If the user submits the registration form
        if request.method == "POST":
            # Retrieve and clean form data
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            # Ensure all required fields are provided
            if not username or not email or not password:
                return render_template(
                    "createaccount.html",
                    error="Please fill in all fields."
                )

            # Prevent duplicate accounts by email
            # include_password=True ensures we fully check existing users
            existing = login_model.get_user_by_email(
                email,
                include_password=True
            )
            if existing:
                return render_template(
                    "createaccount.html",
                    error="Username or email already exists."
                )

            # Create the new user
            # Password hashing is handled inside LoginModel
            login_model.create_user({
                "username": username,
                "email": email,
                "password": password
            })

            # Redirect to login page after successful registration
            return redirect(url_for("login"))

        # GET request: show the registration page
        return render_template("createaccount.html")

    # -------------------- LOGOUT --------------------
    @app.route("/logout")
    def logout():
        """
        Log the user out by clearing the session.
        """
        # Remove all session data (user_id, username, etc.)
        session.clear()

        # Redirect user back to the login page
        return redirect(url_for("login"))

    # -------------------- PROFILE --------------------
    @app.route("/profile")
    def profile():
        """
        Display the user's profile page.

        Requires the user to be logged in.
        """
        # Require authentication
        if "user_id" not in session:
            return redirect(url_for("login"))

        # Fetch the user's data from the database
        user = login_model.get_user_by_id(session["user_id"])
        if not user:
            # If the user no longer exists, clear session and force login
            session.clear()
            return redirect(url_for("login"))

        # Render the profile page with user data
        return render_template("profile.html", user=user)
