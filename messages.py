from db import db
import users

def get_list():
    sql = "SELECT M.content, U.username, M.created_at, M.user_id, M.id FROM messages M, users U " \
          "WHERE M.user_id=U.id AND M.visible=true ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_with_invisible():
    sql = "SELECT M.content, U.username, M.created_at, M.user_id, M.id, M.visible FROM messages M, users U " \
          "WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, created_at, visible) VALUES (:content, :user_id, NOW(), true)"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def get_user_id(id):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def hide(id):    
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == get_user_id(id):
        allow = True
    
    print("logged user: "+str(users.user_id())+"; message sender: "+str(get_user_id(id)))
    
    if allow:
        sql = "UPDATE messages SET visible=false WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    else:
        return False