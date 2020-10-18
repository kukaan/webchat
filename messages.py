from db import db
import users

def get_list():
    sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id 
             FROM messages M, users U 
             WHERE M.user_id=U.id AND M.visible=true 
             ORDER BY M.id"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_with_invisible():
    sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, M.visible 
             FROM messages M, users U 
             WHERE M.user_id=U.id 
             ORDER BY M.id"""
    result = db.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """INSERT INTO messages (content, user_id, created_at, visible) 
             VALUES (:content, :user_id, NOW(), true)"""
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
    
    if allow:
        sql = "UPDATE messages SET visible=false WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    else:
        return False

def result(query, order):
    if order == "ASC":
        if users.is_admin():
            sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, 
                    M.visible, T.topic, T.id, M.edited_at 
                 FROM messages M, users U, threads T 
                 WHERE (M.content ILIKE :query OR T.topic ILIKE :query) AND M.user_id=U.id AND M.thread_id=T.id 
                 ORDER BY M.created_at ASC"""
        else:
            sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, 
                    M.visible, T.topic, T.id, M.edited_at 
                 FROM messages M, users U, threads T 
                 WHERE (M.content ILIKE :query OR T.topic ILIKE :query) AND M.user_id=U.id AND M.thread_id=T.id 
                 AND M.visible=true 
                 ORDER BY M.created_at ASC"""
    else:
        if users.is_admin():
            sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, 
                    M.visible, T.topic, T.id, M.edited_at 
                 FROM messages M, users U, threads T 
                 WHERE (M.content ILIKE :query OR T.topic ILIKE :query) AND M.user_id=U.id AND M.thread_id=T.id 
                 ORDER BY M.created_at DESC"""
        else:
            sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, 
                    M.visible, T.topic, T.id, M.edited_at 
                 FROM messages M, users U, threads T 
                 WHERE (M.content ILIKE :query OR T.topic ILIKE :query) AND M.user_id=U.id AND M.thread_id=T.id 
                 AND M.visible=true 
                 ORDER BY M.created_at DESC"""

    # this would be better, but doesn't work for some reason
    #sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, 
    #                M.visible, T.topic, T.id, M.edited_at 
    #             FROM messages M, users U, threads T 
    #             WHERE (M.content ILIKE :query OR T.topic ILIKE :query) AND M.user_id=U.id AND M.thread_id=T.id 
    #             AND M.visible=true 
    #             ORDER BY M.created_at :order"""
    #result = db.session.execute(sql, {"query":"%"+query+"%", "order":"%"+order+"%"})

    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def edit_message(id, content):
    allow = False
    if users.user_id() == get_user_id(id):
        allow = True
    if allow:
        sql = "UPDATE messages SET content=:content, edited_at=NOW() WHERE id=:id"
        db.session.execute(sql, {"id":id, "content":content})
        db.session.commit()
        return True
    else:
        return False

def get_message_attributes(id):
    sql = "SELECT content, thread_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_latest_messages():
    sql = """SELECT M.content, U.username, M.created_at, M.user_id, M.id, M.visible, 
                T.topic, T.id, M.edited_at 
             FROM messages M, users U, threads T 
             WHERE M.user_id=U.id AND M.thread_id=T.id AND M.visible=true 
             ORDER BY M.created_at DESC LIMIT 3"""
    result = db.session.execute(sql)
    return result.fetchall()


