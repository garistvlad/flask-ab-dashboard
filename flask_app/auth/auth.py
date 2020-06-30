from flask import Blueprint
from flask import flash
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from .forms import LoginForm, RegistrationForm
from models import User
from main import db


bp = Blueprint(
    "auth",
    __name__
)


@bp.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("ab.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # save user to DB:
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Email: '{form.email.data}' successfully registered. Now you may log in.", category="success")
        
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=('GET', 'POST'))
def login():

    if current_user.is_authenticated:
        return redirect(url_for("ab.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", category="danger")
            return redirect(url_for("auth.login"))
        
        login_user(user, remember=True)
        # redirect for initially requested page:
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ab.index')
        return redirect(next_page)
    
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
