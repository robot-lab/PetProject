from flask import Flask, render_template, flash, redirect, logging, url_for, session, request
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
from forms import RegisterForm, LoginForm


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/events"
app.config["SECRET_KEY"] = "secretkey1234trdkggjdlirgjhui4321"
mongo = PyMongo(app)


@app.route("/")
def index():
    events = mongo.db.events.find()
    return render_template("index.html", events=events)


@app.route("/event/<eventid>")
def event_profile(eventid):
    event = mongo.db.events.find_one_or_404({"id": eventid})
    return render_template("event.html", event=event)


@app.route("/user")
def user_profile():
    events = mongo.db.events.find()
    return render_template("user.html", events=events)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = dict()
        user["name"] = form.name.data
        user["email"] = form.email.data
        user["username"] = form.username.data
        user["password"] = sha256_crypt.encrypt(str(form.password.data))
        mongo.db.users.insert_one(user)
        flash("You are now registered and can log in", "success")
        redirect(url_for("index"))
    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
