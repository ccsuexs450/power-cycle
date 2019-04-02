import sqlite3

conn = sqlite3.connect('cycle.db')
conn.execute("PRAGMA foreign_keys = ON")

print ("Opened database successfully");

conn.execute('''CREATE TABLE user
         (email   TEXT  PRIMARY KEY      NOT NULL,
         fname          TEXT             NOT NULL,
         lname          TEXT             NOT NULL,
         age            INT              NOT NULL,
         height         REAL             NOT NULL,
         weight         REAL             NOT NULL,
         gender         TEXT,
         category       INT);''')

print ("Table created successfully");

conn.execute('''CREATE TABLE text
         (id INTEGER PRIMARY KEY NOT NULL,
         user_email TEXT NOT NULL REFERENCES user(email),
         name            TEXT           NOT NULL,
         path            TEXT           NOT NULL,
         date            DATE           NOT NULL);''')

print ("Table created successfully");

conn.execute('''CREATE TABLE powersheet
         (id INTEGER PRIMARY KEY NOT NULL,
         user_email TEXT NOT NULL REFERENCES user(email),
         name            TEXT          NOT NULL,
         path            TEXT          NOT NULL,
         date            DATE          NOT NULL);''')

print ("Table created successfully");

conn.execute('''CREATE TABLE calibration
         (id INTEGER PRIMARY KEY NOT NULL,
         name            TEXT          NOT NULL,
         path            TEXT          NOT NULL,
         date            DATE          NOT NULL);''')

print ("Table created successfully");

conn.close()
