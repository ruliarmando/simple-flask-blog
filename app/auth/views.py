from flask import request, render_template, flash, redirect, url_for, session, g, Blueprint
from flask.ext.login import current_user, login_user, logout_user, login_required

from app.shared.connection import db
from app.shared.models import User
from app.shared.forms import LoginForm


auth = Blueprint('auth', __name__)

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid Username or Password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        next = request.args.get('next')
        login_user(existing_user)
        return redirect(next or url_for('frontend.index'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash('You have successfully logged out.', 'success')
    logout_user()
    return redirect(url_for('auth.login'))