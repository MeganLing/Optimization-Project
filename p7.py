# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 03:42:37 2018

@author: megan
"""

import mysql.connector
from gurobipy import *
import pandas as pd


db = mysql.connector.connect(user = 'root', password = 'root', host = 'localhost', database = 'optfinal')

cur = db.cursor(buffered=True)


# import dc, store, and mileage data from MySql tables
cur.execute("select * from dc;")
dc = cur.fetchall()
df_dc = pd.DataFrame(dc)  
#print(df_dc) # #of 0dcID ;1 capacity
 
cur.execute("select * from store;")
store = cur.fetchall()
df_store = pd.DataFrame(store)
#print(df_store) # 0 storeID; 1 requirements
df_store[1]

cur.execute("select * from mileage;")
mileage = cur.fetchall()
df_mileage = pd.DataFrame(mileage)
#print(df_mileage) #0 dcID ;1 storeID; 2 mileage

dcid = df_mileage[0]
storeid = df_mileage[1]
mileage_r = df_mileage[2]
requirement = df_store[1]
mileage = df_mileage[2]
capacity = df_dc[1]

cost_m = 0.75
cost_t = 200

# create a 'table' with numdc columns and numstores 
numdc=len(df_dc[0])
numstores =len(df_store[0])
datarange =  numdc * numstores

#Create Gurobi model
from gurobipy import *
m = Model("WW.02") 
m.ModelSense = GRB.MINIMIZE
m.setParam('TimeLimit', 7200)

#create mileage dict
mile = dict()
mile = {(dcid[i], storeid[i]):mileage_r[i] for i in range(len(mileage_r))}
#print(trailers_dic)

#Create variables; g stands for binary variable go_or_not>; 
g = {}
trailers = {}
for i in range(numdc):
    for j in range(numstores):
        g[(i,j)] = m.addVar(vtype = GRB.BINARY,name= "pair%s%s" % (i,j))
        
m.update()

#Objective 
m.setObjective(0.75*quicksum(g[(i,j)]*mile[(i,j)] for i in range(numdc) for j in range(numstores))+sum(g[(i,j)] for i in range(numdc) for j in range(numstores))*200, GRB.MINIMIZE)

m.update()

# constrains 
for i in range(numstores):
    shipments = []
    for key in g:
        if key [-1] == storeid[i]:
            shipments.append(g[key])
    m.addConstr(sum(shipments), GRB.EQUAL, 1)
m.update()

for i in range(numdc):
    y = []
    for key in g:
        if key[0] == dcid[i]:
            y.append(g[key])
    m.addConstr(quicksum(y[i]*requirement[j] for j in range(numstores)), GRB.LESS_EQUAL, 12000)
m.update()

# result
m.optimize()

target = []
for key, value in g.items():
    if value.x == 1:
        target.append([key[0],key[1]])
#print(target)

# write out results
for [i,j] in target:
    cur.execute('insert into results (dc_id, store_id) values (%s, %s)', (i,j))
    
db.commit()
