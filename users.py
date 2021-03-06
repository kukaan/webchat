from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, is_admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["is_admin"] = user[2]
            return True
        else:
            return False

def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password, is_admin) 
                 VALUES (:username, :password, FALSE)"""
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def is_admin():
    return session.get("is_admin", None)

def username():
    return session.get("username", 0)

def get_user(id):
    sql = "SELECT username, is_admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()