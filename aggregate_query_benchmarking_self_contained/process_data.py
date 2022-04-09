import sqlite3
import pandas as pd

def get_data(path, table_name):
    conn = sqlite3.connect(path) 
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    c.execute('PRAGMA table_info({});'.format(table_name))
    #get columns
    columns = []
    for row in c:
        columns.append(row[1])
    #get users
    data = []
    c.execute('SELECT * FROM {};'.format(table_name))
    i = 0
    for row in c:
        drop = False
        if i % 1000:
            print("Getting data for user: ", i)
        record = {}
        n = 0
        for column in columns:
            if row[n] == None:
                drop = True
            record[column] = row[n]
            n += 1
        i += 1
        if not drop:
            data.append(record)
    return pd.DataFrame(data)

def get_data_csv(path, start, end):
    users = pd.read_csv(path)
    columns = users.columns[1:]
    data = []
    for i in range(start, end + 1):
        row = tuple(users.iloc[[i]].values[0][1:])
        record = {}
        n = 0            
        for column in columns:
            record[column] = row[n]
            n += 1
        data.append(record)
    return data, columns

def collect_all_data():
    paths = ["private_1M_0.1.db",
            "private_1M_0.2.db",
            "private_1M_0.3.db",
            "private_1M_0.4.db",
            "private_1M_0.5.db",
            "private_1M_0.6.db",
            "private_1M_0.7.db",
            "private_1M_0.8.db",
            "private_1M_0.9.db",
            "private_1M_1.0.db",
            "private_1M_1.1.db"]
    dataframes = []
    for path in paths:
        dataframes.append(get_data(path, "Users"))
    df = pd.concat(dataframes)
    df = df.drop_duplicates(subset=['user_id'])
    df.to_csv('private_db_benchmarking_data.csv')
    print("Done!")