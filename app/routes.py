import os
from datetime import datetime
from app import app, db, model_fox, model_guardian, model_nbc, model_processing
from app.email import send_password_reset_email
from app.forms import LoginForm, QueryEditForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.models import User
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("/"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)


@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    return render_template("results.html")

@app.route("/query", methods=["GET", "POST"])
@login_required
def query_add_page():
    form = QueryEditForm()
    if request.method == 'POST':
        return redirect(url_for("processing"))
    return render_template("n_query.html", form=form)

@app.route("/processing", methods=["GET", "POST"])
@login_required
def processing():
    print("Start")
    if request.method == 'GET':
        return render_template('processing.html')
    
    if request.method == 'POST':
        n1 = model_nbc.newsSoupNBC()
        f1 = model_fox.newsSoupFox()
        g1 = model_guardian.newsSoupGuardian()
        print("Instantiated")
        n1.getInfo()
        n1.cleanAll_Tags()
        n1.createDataFrame()
        f1.getInfoh2()
        f1.cleanAll_Tags_h2()
        f1.createDataFrame()
        g1.getInfo()
        g1.cleanAll_Tags()
        g1.createDataFrame()
        p = model_processing.ProcessingFrame()
        p.readingFrames()
        p.applyToFrame()
        print("Cleaning up.")
        for folder, subfolders, files in os.walk('temp/'):
            for file in files:
                if file.endswith('.csv'):
                    path = os.path.join(folder, file)
                    print('deleted : ', path)
                    os.remove(path)
        return "Done" 
        #return render_template('processing.html')

@app.route("/query-results", methods=["GET", "POST"])
@login_required
def query_results():
    return render_template("results.html")

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', 
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.veryify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('home'))
    return render_template('reset_password.html', form=form)