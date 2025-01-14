CREATE TABLE users (
                       userid TEXT PRIMARY KEY,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL
);

CREATE TABLE birthdays (
                           uuid TEXT PRIMARY KEY,
                           name TEXT,
                           date TEXT,
                           userid TEXT,
                           FOREIGN KEY (userid) REFERENCES users(userid)
);