import sqlite3

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print()
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session["user_id"] = None
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    con = sqlite3.connect("regime-forge.db")
    cur = con.cursor()

    if not username:
        return render_template("signup.html", error="Please enter username")

    if not password or not confirmation or password != confirmation:
        return render_template("signup.html", error="Please enter valid password")

    user = {"name": username, "hash": generate_password_hash(password)}
    res = cur.execute("SELECT * FROM users WHERE username = :name", user)
    res = res.fetchone()
    
    if res is not None:
        return render_template("signup.html", error="Username taken")

    cur.execute("INSERT INTO users (username, hash) VALUES (:name, :hash)", user)
    con.commit()

    res = cur.execute("SELECT id FROM users WHERE username = :name", user)
    session["user_id"] = res.fetchone()[0]

    con.close()
    return redirect("/")
