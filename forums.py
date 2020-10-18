from db import db
import users

def get_forums():
    sql = "SELECT id, name, visibility FROM forums F ORDER BY F.name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_forum_threads(id):
    sql = """SELECT T.topic, U.username, T.created_at, T.user_id, T.id, T.visible 
             FROM threads T, users U 
             WHERE T.forum_id=:id AND T.user_id=U.id AND T.visible=true 
             ORDER BY T.created_at DESC"""
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_forum_attributes(id):
    sql = "SELECT name, visibility FROM forums WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def newthread(forum_id, title):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """INSERT INTO threads (topic, user_id, created_at, visible, forum_id) 
             VALUES (:topic, :user_id, NOW(), true, :forum_id)"""
    db.session.execute(sql, {"topic":title, "user_id":user_id, "forum_id":forum_id})
    db.session.commit()
    return True