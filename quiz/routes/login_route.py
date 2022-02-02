from quiz import app
from quiz import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from quiz.forms import *
from quiz.db_models import *
from flask import Flask, render_template, flash, request, redirect, url_for

# Flask login requisites
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create login page
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hashed password
            if check_password_hash(user.password_hash, form.password.data):
                # form.password.data -> user supplied pwd, user.password_hash -> hashed pwd stored in DB for this username
                # if both these matches , then login successful
                login_user(user)
                flash('Login successful !')
                return redirect(url_for('dashboard'))
            else:
                flash('Password incorrect - please give correct password')
        else:
            flash('Username - doesnt exist. Please try again with correct username')

    return render_template('login.html', form=form)

# Create logout page
@app.route('/logout',methods=['GET','POST'])
@login_required # We can't logout unless logged-in
def logout():

    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('login'))

# Create dashboard page
@app.route('/dashboard',methods=['GET','POST'])
@login_required  # This will help reroute back to login page if not logged-in
def dashboard():
    our_users = Users.query.order_by(Users.date_added)
    return render_template('dashboard.html',
                           our_users=our_users)

#Create route decorator
@app.route('/')
def index():
    message = ' <strong> Welcome...If new user, Please go to Register tab to sign-up </strong>'
    return render_template("index.html",
                           message = message,
                           )