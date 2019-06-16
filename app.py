from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://virrius:QWErty@cluster0-2yjj1.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/event/<eventname>")
def event_profile(eventname):
    event = mongo.db.events.find_one_or_404({"_id": eventname})
    return render_template("event.html", event=event)
