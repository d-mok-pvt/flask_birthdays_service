-- CREATE TABLE birthdays (
--         id INTEGER,
--         name TEXT,
--         date TEXT, uuid TEXT,
--         CONSTRAINT BIRTHDAYS_PK PRIMARY KEY (id)
-- );

CREATE TABLE birthdays (
        uuid TEXT PRIMARY KEY,
        name TEXT,
        date TEXT
);
