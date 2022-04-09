#imports for server
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import requests
#imports for database
import sqlite3
from set_up import set_up_system
from utils import execute_query
import json
import sqlparse
from sql_metadata import Parser



#---------------------------------- SET UP SYSTEM --------------------------------------
#app = Flask(__name__)
#CORS(app)
#conn_s, c_s, conn_gb, c_gb = set_up_system()
#---------------------------------------------------------------------------------------

#---------------------------------- INIT APP -------------------------------------------
app = Flask(__name__)
CORS(app)
conn_gb = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\global_db\\venv\\data\\gb_data.db', check_same_thread=False)
c_gb = conn_gb.cursor()
conn_s = sqlite3.connect('C:\csystems\\reactjs\\prototype1\\src\\global_db\\venv\\data\\schema.db', check_same_thread=False)
c_s = conn_s.cursor()
r = requests.post("http://localhost:5000/init_command")
assert r.status_code == 200, "Microdbs cluster did not init properly"
aggregate_queries = {}
#---------------------------------------------------------------------------------------

@app.route("/who_request", methods=['POST', 'GET'])
@cross_origin(origin='localhost', headers=['Content-type'])
def who_request():
    #determine if this is a valid request based on schema
    query = request.json["query"]
    try:
        c_s = conn_s.cursor()
        c_s.execute(query)
    except sqlite3.OperationalError:
        return {"response": "Global DB here :) - who request! - invalid query", "queryResult": "None", "who": "None"}

    #determine if this query can be executed in gdb
    try: 
        #attempt to execute query
        c_gb = conn_gb.cursor()
        c_gb.execute(query)
        fields = [field_meta[0] for field_meta in c_gb.description]
        response = [dict(zip(fields,row)) for row in c_gb.fetchall()]
        return {"response": "Global DB here :) - query accepted", "queryResult": json.dumps(response), "who": "gdb"}
    except sqlite3.OperationalError:
        #check if this an implemented and valid aggregate query 
        if sqlparse.parse(query)[0][2].get_name() == "count" or \
        sqlparse.parse(query)[0][2].get_name() == "COUNT" or \
        sqlparse.parse(query)[0][2].get_name() == "Count":
            return handle_aggregate_request(query)
        else:
            return {"response": "Global DB here :) - send request to mdb", "queryResult": "None", "who": "mdb"}


def handle_aggregate_request(query):
    if query not in aggregate_queries:
        c_gb = conn_gb.cursor()
        c_gb.execute("SELECT user_id from Users;")
        users = []
        for u in c_gb:
            users.append(u)
        #------------------------------PROTECTED AREA ------------------------------
        count = 0
        for u in users:
            r = requests.post("http://localhost:{}/aggregate_request".format(u[0]),
                    json={"query": query})
            count = count + float(r.json()["result"])
        #----------------------------- END OF PROTECTED AREA -------------------------
        aggregate_queries[query] = count
        return {"response": "Global DB here :) - aggregate request!", "queryResult": "{'count':"+ str(count) + "}", "who": "system"}
    else:
        count = aggregate_queries[query]
        return {"response": "Global DB here :) - aggregate request!", "queryResult": "{'count': "+ str(count) + "}", "who": "system"}

@app.route("/micro_db_request", methods=['POST', 'GET'])
@cross_origin(origin='localhost',headers=['Content-type'])
def micro_db_request():
    #TODO: Implement
    return {"response": "Global DB here :) - micro_db request!"}
