import os
from datetime import datetime
from app import app, model_fox, model_guardian, model_nbc, model_processing
from app.forms import LoginForm, QueryEditForm
from flask import (Flask, flash, redirect, render_template, request, url_for)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route("/results", methods=["GET", "POST"])
def results():
    return render_template("results.html")

@app.route("/query", methods=["GET", "POST"])
def query_add_page():
    form = QueryEditForm()
    if request.method == 'POST':
        return redirect(url_for("processing"))
    return render_template("n_query.html", form=form)

@app.route("/processing", methods=["GET", "POST"])
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
def query_results():
    return render_template("results.html")
