import sqlite3
import os

def set_up_micro_db():
    """SET UP: 
    Example is based on a simple social media web app.
    All values are expected to either be private or public.
    Public values are stored in micro_db.db.
    The micro database (mdb) contains a schema in schema.db of all data stored in the system.
    Returns: connection for micro_db, cursor for micro_db, connection for schema, cursor for schema
    """
    #------------------------------------ SET UP micro_db ------------------------------
    #figure out which micro_db you are
    arr = os.listdir('C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data')
    if len(arr) == 0:
        port = 5000
    else:
        port = 5000 + len(arr)//2 

    #initialize connection to micro_db
    conn_mdb = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\micro_db_{}.db'.format(port), check_same_thread=False)
    c_mdb = conn_mdb.cursor()
    # create users table
    create_users_table_command = '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT NOT NULL,
        first_name varchar(255) NOT NULL,
        surname varchar(255) NOT NULL,
        phone int, 
        email varchar(255) NOT NULL,
        password varchar(255) NOT NULL,
        day int NOT NULL,
        month int NOT NULL, 
        year int NOT NULL, 
        gender varchar(255),
        location varchar(255), 
        PRIMARY KEY (user_id));'''
    c_mdb.execute(create_users_table_command)
    conn_mdb.commit()
    # create friends table
    create_friends_table_command = '''
    CREATE TABLE IF NOT EXISTS Friends (
        user_id1 INT NOT NULL,
        user_id2 INT NOT NULL,
        PRIMARY KEY (user_id1, user_id2),
        FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE SET NULL);
    '''
    c_mdb.execute(create_friends_table_command)
    conn_mdb.commit()
    # create likes table
    create_likes_table_command = '''
    CREATE TABLE IF NOT EXISTS Likes (
        user_id1 INT NOT NULL,
        user_id2 INT NOT NULL,
        post_id INT NOT NULL,
        PRIMARY KEY (user_id1, user_id2, post_id),
        FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE SET NULL);
    '''
    c_mdb.execute(create_likes_table_command)
    conn_mdb.commit()
    #------------------------------------ SET UP schema ------------------------------
    #initialize connection to schema
    conn_schema = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\schema_{}.db'.format(port), check_same_thread=False)
    c_schema = conn_schema.cursor()
    # create users table
    create_users_table_command = '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT NOT NULL,
        first_name varchar(255) NOT NULL,
        surname varchar(255) NOT NULL,
        phone int, 
        email varchar(255) NOT NULL,
        password varchar(255) NOT NULL,
        day int NOT NULL,
        month int NOT NULL, 
        year int NOT NULL, 
        gender varchar(255),
        location varchar(255), 
        PRIMARY KEY (user_id));'''
    c_schema.execute(create_users_table_command)
    conn_schema.commit()
    # create friends table
    create_friends_table_command = '''
    CREATE TABLE IF NOT EXISTS Friends (
        user_id1 INT NOT NULL,
        user_id2 INT NOT NULL,
        PRIMARY KEY (user_id1, user_id2),
        FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE SET NULL);
    '''
    c_schema.execute(create_friends_table_command)
    conn_schema.commit()
    # create likes table
    create_likes_table_command = '''
    CREATE TABLE IF NOT EXISTS Likes (
        user_id1 INT NOT NULL,
        user_id2 INT NOT NULL,
        post_id INT NOT NULL,
        PRIMARY KEY (user_id1, user_id2, post_id),
        FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE SET NULL);
    '''
    c_schema.execute(create_likes_table_command)
    conn_schema.commit()
    return conn_mdb, c_mdb, conn_schema, c_schema
