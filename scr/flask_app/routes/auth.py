from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import LoginForm
from ..models import User
from scr.database.database import Database

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data)
        if user is not None and User.verify_password(user, form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Log the login activity
            db = Database()
            db.add_activity_log(
                activity_type="LOGIN",
                description=f"User {user.username} logged in",
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                username=user.username
            )
            
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('index.home')
            return redirect(next_page)
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form, title='Sign In')

@auth.route('/logout')
@login_required
def logout():
    # Log the logout activity
    db = Database()
    db.add_activity_log(
        activity_type="LOGOUT",
        description=f"User {current_user.username} logged out",
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        username=current_user.username
    )
    
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login')) 