from app import app

from flask import render_template, jsonify

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/ping')
def ping():
    return jsonify("pong")
