from flask import Flask, render_template, url_for, request
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")


