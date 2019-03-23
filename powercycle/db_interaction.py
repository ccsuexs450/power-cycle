import sqlite3

# create connection
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

# create user
def create_user(conn, user):

    sql = ''' INSERT INTO user(email, fname, lname, age, height, weight, gender, category)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

# create textfile
def create_textfile(conn, textfile):
    sql = ''' INSERT INTO  text(user_email, name, path, date)
              VAlUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, textfile)
    return cur.lastrowid

## Called from GUI.py user insertion
def user_insert(email, fname, lname, age, height, weight, gender, category):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new user
        user = (email, fname, lname, age, height, weight, gender, category)
        user_rid = create_user(conn, user)

## Called from run_sensor.py
def textfile_insert(user_email, name, path, date):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new user
        textfile = (user_email, name, path, date);
        text_rid = create_textfile(conn, textfile)
