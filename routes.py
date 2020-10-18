from app import app
from flask import render_template, redirect, request
import messages, users, threads, forums

def append_string_length_error(list, string, stringname, min_length, max_length):
    if len(string) < min_length:
        list.append(f"The {stringname} is too short")
    elif len(string) > max_length:
        list.append(f"The {stringname} is too long")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    error_messages = []
    append_string_length_error(error_messages, content, "message", 1, 1000)
    if len(error_messages) > 0:
        return render_template("error.html", messages=error_messages)
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to send the message.")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error_messages = []
        append_string_length_error(error_messages, username, "username", 1, 50)
        append_string_length_error(error_messages, password, "password", 1, 50)
        if len(error_messages) > 0:
            return render_template("error.html", messages=error_messages)
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error_messages = []
        append_string_length_error(error_messages, username, "username", 4, 30)
        append_string_length_error(error_messages, password, "password", 8, 30)
        if len(error_messages) > 0:
            return render_template("error.html", messages=error_messages)
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed.")

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
        if user == None:
            return render_template("error.html", 
                    message=f"No user with id {id} exists.")
        username = user[0]
        is_admin = user[1]
        return render_template("profile.html", 
                user_id=id, username=username, is_admin=is_admin)
    else:
        return render_template("error.html", 
                message="Your account has insufficient rights to view this page.")

@app.route("/deletemessage/<int:id>")
def deletemessage(id):
    if messages.hide(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Message deletion failed.")

@app.route("/thread/<int:id>")
def thread(id):
    if users.is_admin():
        list = threads.get_thread_with_invisible(id)
    else:
        list = threads.get_thread(id)
    thread_attributes = threads.get_thread_attributes(id)
    return render_template("thread.html", count=len(list), messages=list, id=id, 
            thread_attributes=thread_attributes)

@app.route("/threads")
def get_threads():
    if users.is_admin():
        list = threads.get_threads_with_invisible()
    else:
        list = threads.get_threads()
    return render_template("threads.html", count=len(list), threads=list)

@app.route("/thread/<int:id>/delete")
def deletethread(id):
    if threads.hide_thread(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Thread deletion failed.")

@app.route("/thread/<int:id>/reply", methods=["POST"])
def reply(id):
    content = request.form["content"]
    error_messages = []
    append_string_length_error(error_messages, content, "message", 1, 1000)
    if len(error_messages) > 0:
        return render_template("error.html", messages=error_messages)
    if threads.reply(id, content):
        return redirect("/thread/"+str(id))
    else:
        return render_template("error.html", message="Sending message failed.")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/result")
def result():
    query = request.args["query"]
    order = request.args["order"]
    list = messages.result(query, order)
    return render_template("result.html", query=query, order=order, count=len(list), 
            messages=list)

@app.route("/editmessage/<int:id>", methods=["GET", "POST"])
def editmessage(id):
    attributes = messages.get_message_attributes(id)
    if request.method == "GET":
        return render_template("editmessage.html", id=id, content=attributes[0])
    if request.method == "POST":
        content = request.form["content"]
        error_messages = []
        append_string_length_error(error_messages, content, "message", 1, 1000)
        if len(error_messages) > 0:
            return render_template("error.html", messages=error_messages)
        if messages.edit_message(id, content):
            return redirect("/thread/"+str(attributes[1]))
        else:
            return render_template("error.html", message="Failed to edit the message.")

@app.route("/")
def index():
    latest = messages.get_latest_messages()
    forum_list = forums.get_forums()
    return render_template("index.html", count=len(latest), messages=latest, 
            forums=forum_list)

@app.route("/forum/<int:id>")
def forum(id):
    threads = forums.get_forum_threads(id)
    attributes = forums.get_forum_attributes(id)
    return render_template("forum.html", count=len(threads), threads=threads, id=id, 
            attributes=attributes)

@app.route("/forum/<int:id>/newthread", methods=["POST"])
def forum_newthread(id):
    content = request.form["content"]
    error_messages = []
    append_string_length_error(error_messages, content, "message", 1, 60)
    if len(error_messages) > 0:
        return render_template("error.html", messages=error_messages)
    if forums.newthread(id, content):
        return redirect("/forum/"+str(id))
    else:
        return render_template("error.html", message="Thread creation failed failed.")