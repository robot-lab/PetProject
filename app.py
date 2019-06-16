from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://virrius:QWErty@cluster0-2yjj1.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/")
def index():
    events = mongo.db.events.find()
    return render_template("index.html", events=events)


@app.route("/event.html/<eventid>")
def event_profile(eventid):
    event = mongo.db.events.find_one_or_404({"id": eventid})
    return render_template("event.html", event=event)


@app.route("/user.html")
def user_profile():
    events = mongo.db.events.find()
    return render_template("user.html", events=events)
