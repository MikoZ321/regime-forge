from flask import Flask, render_template, request, session
from flask_session import Session

from helper.py import login_required


app = Flask(__name__)

@app.route('/')
@login_required
def hello_world():
    return render_template("layout.html")