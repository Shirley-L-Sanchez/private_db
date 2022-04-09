import sqlite3

def start_app():
    #figure out which micro_db you are
    log_path = 'C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\current_next_port.txt'
    try: 
        f = open(log_path,"r")
        content = f.read()
        port = 5000 if content == "" else content
    except FileNotFoundError:
        f = open(log_path,"w")
        port = 5000
    f.close()

    f = open(log_path,"w")
    f.write(str(int(port) + 1))
    f.close()

    conn_mdb = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\micro_db_{}.db'.format(port), check_same_thread=False)
    c_mdb = conn_mdb.cursor()
    conn_s = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\schema_{}.db'.format(port), check_same_thread=False)
    c_s = conn_s.cursor()
    return conn_mdb, c_mdb, conn_s, c_s