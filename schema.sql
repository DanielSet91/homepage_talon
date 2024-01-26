CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    favorite_genres TEXT,
    favorite_instrument TEXT,
    job TEXT,
    user_id INTEGER,
    twitter TEXT,
    facebook TEXT,
    instagram TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);