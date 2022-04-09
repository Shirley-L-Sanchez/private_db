#import for server
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from set_up import set_up_micro_db
from start_app import start_app
#import for db
import sqlite3
import os
import sys
import numpy as np
import random
import json

#----------------------------------- SET UP APP -----------------------------------
#app = Flask(__name__)
#CORS(app)
#conn_mdb, c_mdb, conn_s, c_s = set_up_micro_db()
#epsilon = 0.1
#----------------------------------------------------------------------------------

#----------------------------------- START APP ------------------------------------
app = Flask(__name__)
CORS(app)
conn_mdb, c_mdb, conn_s, c_s = start_app()
epsilon = 0.1
N = 5
#----------------------------------------------------------------------------------

@app.route("/set_up", methods=['POST', 'GET'])
@cross_origin(origin='localhost')
def set_up():
    #SET UP instructions are ASSUMED to be safe when they come from localhost
    c_mdb.execute(str(request.json["data"]))
    conn_mdb.commit()
    return {"response": "MicroDB here :) - received my data!: " 
    + request.json["data"]}

@app.route("/init_command", methods=['POST', 'GET'])
@cross_origin(origin='localhost:3000')
def init_command():
    #clean log data for next reboot
    log_path = '''C:\csystems\\reactjs\\prototype1\\src\\micro_db\\data\\current_next_port.txt'''
    f = open(log_path,"w")
    f.write("")
    f.close()
    return {"response": "MicroDB here :) - everything set!"}

@app.route("/private_request", methods=['POST', 'GET'])
@cross_origin(origin='localhost', headers=['Content-type'])
def private_request():
    #try:
        #attempt to execute query
        c_mdb = conn_mdb.cursor()
        c_mdb.execute(request.json["query"])
        fields = [field_meta[0] for field_meta in c_mdb.description]
        response = [dict(zip(fields,row)) for row in c_mdb.fetchall()]
        #assert False, response
        return {"response": "MDB DB here :) - query accepted", "queryResult": json.dumps(response), "who": "mdb"}
    #except sqlite3.OperationalError:
        #this shouldn't happen? (at least in model where mdb has all user_related data)
        #assert(False)
    #    return {"response": "MicroDB here :) - private request!" , "queryResult": "None", "who": "None"}

@app.route("/aggregate_request", methods=['POST', 'GET'])
@cross_origin(origin='localhost',headers=['Content-type'])
def aggregate_request():
    c_mdb = conn_mdb.cursor()
    c_mdb.execute(request.json["query"])
    for r in c_mdb:
        count = int(r[0]) #+ np.random.gamma(1/N, 1/epsilon) - np.random.gamma(1/N, 1/epsilon)
    return {"response": "MicroDB here :) - aggregate request!", "result": count}