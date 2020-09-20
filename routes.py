from app import app
from flask import render_template, redirect, request
import messages, users

@app.route("/")
def index():
    if users.is_admin():
        list = messages.get_list_with_invisible()
    else:
        list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if len(content) > 1000:
        return render_template("error.html", message="The message is too long")
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html",message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 30:
            return render_template("error.html", message="The username is too long")
        if len(password) > 30:
            return render_template("error.html", message="The password is too long")
        if len(password) < 8:
            return render_template("error.html", message="The password is too short")
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/myprofile")
def myprofile():
    id = users.user_id()
    return redirect("/profile/"+str(id))

@app.route("/profile/<int:id>")
def profile(id):
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == id:
        allow = True
    if allow:
        user = users.get_user(id)
        #TODO: check that user_id exists
        username = user[0]
        is_admin = user[1]
        return render_template("profile.html", user_id=id, username=username, is_admin=is_admin)
    else:
        return render_template("error.html",message="Ei oikeutta nähdä sivua")

@app.route("/deletemessage/<int:id>")
def deletemessage(id):
    if messages.hide(id):
        return redirect("/")
    else:
        return render_template("error.html",message="Message deletion failed")

@app.route("/thread/<int:id>")
def thread(id):
    if users.is_admin():
        list = messages.get_thread_with_invisible(id)
    else:
        list = messages.get_thread(id)
    thread_attributes = messages.get_thread_attributes(id)
    return render_template("thread.html", count=len(list), messages=list, id=id, thread_attributes=thread_attributes)

@app.route("/newthread", methods=["GET","POST"])
def newthread():
    if request.method == "GET":
        return render_template("newthread.html")
    if request.method == "POST":
        topic = request.form["topic"]
        if len(topic) > 30:
            return render_template("error.html", message="The topic is too long")
        if messages.add_thread(topic):
            return redirect("threads")
        else:
            return render_template("error.html",message="Thread creation failed")

@app.route("/threads")
def threads():
    if users.is_admin():
        list = messages.get_threads_with_invisible()
    else:
        list = messages.get_threads()
    return render_template("threads.html", count=len(list), threads=list)

@app.route("/thread/<int:id>/delete")
def deletethread(id):
    if messages.hide_thread(id):
        return redirect("threads")
    else:
        return render_template("error.html",message="Thread deletion failed")

@app.route("/thread/<int:id>/reply", methods=["POST"])
def reply(id):
    content = request.form["content"]
    if messages.reply(id, content):
        return redirect("/thread/"+str(id))
    else:
        return render_template("error.html",message="Sending message failed")