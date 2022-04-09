import sqlite3
import random
import string
from datetime import datetime
from random_address import real_random_address
import names
from itertools import combinations
from itertools import permutations
import requests

def set_up_schema():
    """SET UP: 
    Example is based on a simple social media web app.
    All values are expected to either be private or public.
    Public values are stored in gb_data.db.
    The global database (gdb) contains a schema in schema.db of all data stored in the system.
    No actual data is stored in schema.db
    This is equivalent to the SQL schema the client sees. 
    Returns: connection for schema, cursor for schema, connection for gdb, cursor for gdb
    """
    #--------------------------------- SET UP global database ---------------------------
    #initialize connection to global db
    conn_gb = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\global_db\\venv\\data\\gb_data.db')
    c_gb = conn_gb.cursor()
    # create users table
    create_users_table_command = '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT PRIMARY KEY NOT NULL,
        first_name varchar(255) NOT NULL,
        surname varchar(255) NOT NULL);'''
    c_gb.execute(create_users_table_command)
    conn_gb.commit()
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
    c_gb.execute(create_likes_table_command)
    conn_gb.commit()
    #------------------------------------ SET UP schema ------------------------------
    #initialize connection to schema
    conn_schema = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\global_db\\venv\\data\\schema.db')
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
    return conn_schema, c_schema, conn_gb, c_gb

def set_up_data(conn_gb, c_gb, N=5, L=10, F=10):
    """
    Inputs: connection for gdb, and cursor for gdb from set_up_schema(); 
    N is the # of users;
    L is the # of likes;
    F is the # of friendships
    """
    def generate_random_user():
        id = int("".join([str(random.randint(0,9)) for i in range(9)]))
        phone = int(''.join(str(random.randint(0, 9)) for i in range(10)))
        email = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(7, 20))) + "@gmail.com"
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(10, 20)))
        day = random.choice(range(1,31))
        month = random.choice(range(1,12))
        year = random.choice(range(datetime.now().year - 100, datetime.now().year))
        #the following is just for testing purposes and is not intended to be inclusive yet
        gender = random.choice(["female", "male"])
        name = names.get_first_name(gender=gender)
        surname = names.get_last_name()
        address_dict = real_random_address()
        location = "".join(address_dict['address1'] + ", " + address_dict['city'] + ", " + address_dict['state'])
        return (id, name, surname, phone, email, password, day, month, year, gender, location)
    
    def insert_users_in_system(n):
        for i in range(n):
            user = generate_random_user()
            #replace user_id with port number -- prototype only
            user_port = 5000 + i
            c_gb.execute(
                '''INSERT INTO Users VALUES 
                (?, ?, ?);''', (user_port,) + user[1:3])
            #--------------- SEND SETUP DATA TO MICRODB ---------------------
            user_data = '''
            INSERT INTO Users VALUES ({}, {}, {}, {}, {},
            {}, {}, {}, {}, {}, {});'''.format(user_port, "'" + user[1] + "'", 
            "'" + user[2] + "'", user[3], "'" + user[4] + "'", "'" + user[5] + "'", user[6], user[7], user[8],
            "'" + user[9] + "'", "'" + user[10] + "'")
            r = requests.post("http://localhost:{0}/set_up".format(user_port),
                json={"data": user_data})
            assert r.status_code == 200, "Data did not reach micro_db in port {}, user_data: {}".format(user_port, user_data)
        conn_gb.commit()

    def insert_likes(n):
        users = []
        c_gb.execute('''SELECT * FROM USERS;''')
        for row in c_gb:
            users.append(row[0])
        all_possible_likes = list(permutations(users, 2))
        records = []
        for i in range(n):
            like_pair = random.choices(all_possible_likes, k=1)[0]
            post_id = int(''.join(str(random.randint(0, 9)) for i in range(10)))
            if (like_pair[0], like_pair[1], post_id) not in records:
                c_gb.execute('''INSERT INTO Likes VALUES (?, ?, ?);''', (like_pair[0], like_pair[1], post_id))
                records.append((like_pair[0], like_pair[1], post_id))
                #--------------- SEND SETUP DATA TO MICRODB ---------------------
                user_data = '''
                INSERT INTO Likes VALUES ({}, {}, {});'''.format(like_pair[0], like_pair[1], post_id)
                r = requests.post("http://localhost:{}/set_up".format(like_pair[0]),
                    json={"data": user_data})
                assert r.status_code == 200, "Data did not reach micro_db in port {}".format(like_pair[0])
                #DUPLICATE DATA
                r = requests.post("http://localhost:{}/set_up".format(like_pair[1]),
                    json={"data": user_data})
                assert r.status_code == 200, "Data did not reach micro_db in port {}".format(like_pair[1])
        conn_gb.commit()
    
    def insert_friends(n):
        users = []
        c_gb.execute('''SELECT * FROM USERS;''')
        for row in c_gb:
            users.append(row[0])
        all_possible_friendships = list(combinations(users, 2))
        for i in range(n):
            friend_pair = random.sample(all_possible_friendships, k=1)[0]
            all_possible_friendships.remove(friend_pair)
            #--------------- SEND SETUP DATA TO MICRODB ---------------------
            user_data = '''
            INSERT INTO Friends VALUES ({}, {});'''.format(friend_pair[0], friend_pair[1])
            r = requests.post("http://localhost:{}/set_up".format(friend_pair[0]),
                json={"data": user_data})
            assert r.status_code == 200, "Data did not reach micro_db in port {}".format(friend_pair[0])
            #DUPLICATE DATA
            r = requests.post("http://localhost:{}/set_up".format(friend_pair[1]),
                json={"data": user_data})
            assert r.status_code == 200, "Data did not reach micro_db in port {}".format(friend_pair[1])


    insert_users_in_system(N)
    insert_likes(L)
    insert_friends(F)

def set_up_system():
    conn_schema, c_schema, conn_gb, c_gb = set_up_schema()
    set_up_data(conn_gb, c_gb)
    return conn_schema, c_schema, conn_gb, c_gb