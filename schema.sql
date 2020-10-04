CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);
CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visibility INTEGER
);
CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    edited_at TIMESTAMP,
    visible BOOLEAN,
    forum_id INTEGER REFERENCES forums
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    edited_at TIMESTAMP,
    visible BOOLEAN,
    thread_id INTEGER REFERENCES threads
);

