from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from app.extensions.database.models import User
from app.extensions.database.database import db
from .controllers import UserController

blueprint = Blueprint("user", __name__)
user_controller = UserController()


@blueprint.route("/")
def index():
    return render_template("user/index.html")


@blueprint.get("/login")
def get_login():
    return render_template("user/login.html")


@blueprint.post("/login")
def post_login():
    try:
        user = user_controller.get_user_by_email(request.form.get("email"))

        if not user:
            raise Exception("No user with the given email address was found.")
        if not user.check_password(request.form.get("password")):
            raise Exception("The password does not appear to be correct.")

        login_user(user)

        return redirect(url_for("subjects.all_subjects"))

    except Exception as error_message:
        error = (
            error_message
            or "An error occurred while logging in. Please verify your email and password."
        )
        return render_template("user/login.html", error=error)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.get_login"))


@blueprint.get("/register")
def get_register():
    return render_template("user/registration.html")


@blueprint.post("/register")
def post_register():
    try:
        if request.form.get("password") != request.form.get("password_confirmation"):
            return render_template(
                "user/registration.html",
                error="The password confirmation must match the password.",
            )
        if user_controller.get_user_by_email(request.form.get("email")):
            return render_template(
                "user/registration.html",
                error="The email address is already registered.",
            )

        user = user_controller.add_user(
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("fname"),
        )

        login_user(user)

        return redirect(url_for("subjects.all_subjects"))

    except Exception as error_message:
        error = (
            error_message
            or "An error occurred while creating a user. Please make sure to enter valid data."
        )
        return render_template("user/registration.html", error=error)
