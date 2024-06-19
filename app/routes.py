from datetime import datetime
from app import app, db, model_call, mail
from app.email import send_password_reset_email
from app.forms import ContactForm, LoginForm, PersistentSearchForm, QuickSearchForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.models import PersistentQuery, User
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/home")
def home():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """  
        From: %s <%s>  
        %s  
        """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == 'GET':
    return render_template('contact.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("/"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.info('%s failed to log in', form.username.data)
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            app.logger.info('%s logged in successfully', form.username.data)
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
        user = User(firstname=form.firstname.data, 
                    lastname=form.lastname.data, 
                    username=form.username.data, 
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)

@app.route("/quicksearch", methods=["GET", "POST"])
@login_required
def quicksearch():
    form = QuickSearchForm()
    if request.method == 'POST':
        file_y = open('temp/AnySearchterms.txt', 'w')
        file_l = open('temp/AllSearchterms.txt', 'w')
        san = form.searchtermsAny.data
        sal = form.searchtermsAll.data
        file_y.write(san)
        file_y.close()
        file_l.write(sal)
        file_l.close()
        return redirect(url_for("processing"))
    return render_template("quicksearch.html", form=form)

@app.route("/processing", methods=["GET", "POST"])
@login_required
def processing():
    print("Start")
    if request.method == 'GET':
        return render_template('processing.html')

    if request.method == 'POST':
        m = model_call.RunModels()
        m.modelCall()
        return "Done" 

@app.route("/quicksearch_results", methods=["GET", "POST"])
@login_required
def quicksearch_results():
    return render_template("qicksearch_results.html")

@app.route("/persistentsearch")
@login_required
def persistentSearch():
    form = PersistentSearchForm()
    if form.validate_on_submit():
        query = PersistentQuery(query_name=form.query_name.data, 
                                searchtermsAny=form.searchtermsAny.data,
                                searchtermsAll=form.searchtermsAll.data)
        db.session.add(query)
        db.session.commit()
        flash(f"Congratulations, you submitted {form.query_name.data} for processing!")
        return redirect(url_for("processing"))
    return render_template("persistentsearch.html", form=form)

@app.route("/persistent_results", methods=["GET", "POST"])
@login_required
def persistentSearch_results():
  return render_template("persistent_results.html")


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