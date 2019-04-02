import sqlite3

# create connection
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
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

# create calibration_file
def create_calibrate(conn, spreadsheet):
    sql = ''' INSERT INTO  calibration(name,path,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, spreadsheet)
    return cur.lastrowid

# search email
def email_select(conn, email):
    sql = ''' SELECT email FROM user WHERE email=? '''
    cur = conn.cursor()
    cur.execute(sql, (email,))
    return cur.fetchone()

# Called from GUI.py user insertion
def user_insert(email, fname, lname, age, height, weight, gender, category):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new user
        user = (email, fname, lname, age, height, weight, gender, category)
        user_rid = create_user(conn, user)

# Called from calibrate.py

def calibrate_insert(name, path, date):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new spreadsheet
        spreadsheet = (name, path, date)
        calibrate_rid = create_calibrate(conn, spreadsheet)

# Called from run_sensor.py
def textfile_insert(user_email, name, path, date):

    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # new textfile
        textfile = (user_email, name, path, date)
        text_rid = create_textfile(conn, textfile)


# Called from GUI.py email search window
def email_search(email):
   
    database = 'cycle.db'
    
    # database connection
    conn = create_connection(database)
    with conn:
        # search for email
        search_result = email_select(conn, email)

    return search_result


# search file
def file_select(conn, name):
    sql = ''' SELECT * FROM text WHERE name=? '''
    cur = conn.cursor()
    cur.execute(sql, (name, ))
    return cur.fetchall()


# Called from GUI.py file search window
def file_search(name):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search for file
        search_result = file_select(conn, name)

    return search_result


# search user by first name
def user_select(conn, fname):
    sql = ''' SELECT * FROM user WHERE fname=?'''
    cur = conn.cursor()
    cur.execute(sql, (fname,))
    return cur.fetchall()


# Called from GUI.py file search window
def user_search(fname):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search for user
        search_result = user_select(conn, fname)

    return search_result


# search file by date
def file_date_select(conn, name):
    sql = ''' SELECT * FROM text WHERE name=?'''
    cur = conn.cursor()
    cur.execute(sql, (name,))
    return cur.fetchall()


# Called from GUI.py file search window
def file_date_search(name):
    database = 'cycle.db'

    # database connection
    conn = create_connection(database)
    with conn:
        # search for file by date
        search_result = file_date_select(conn, name)

    return search_result
