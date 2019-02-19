# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 01:40:39 2018

@author: megan
"""
from gurobipy import *

#create Gurobi model
m = Model("WW") 
m.ModelSense = GRB.MINIMIZE
m.setParam('TimeLimit', 7200)

#Facts
mileage = [102.6070194,981.5160308,889.4214567,720.9953667,363.4673676,452.6908275,563.9138436,155.4318437,
570.9344692,806.0617236,199.2023744,986.1157401,867.4985554,340.584254,113.3047579,312.6843448]
requirement = [208,54,66,282]
cost_m = 0.75
cost_t = 200

#variables
g = []
trailers = [] # set variables for go_or_not & #of trailers
for i in range(len(mileage)):
    g.append(m.addVar(vtype = GRB.BINARY, lb = 0, ub = 1))
    trailers.append(m.addVar(vtype = GRB.INTEGER, lb=0))
m.update()

#Objective 
m.setObjective(quicksum(trailers[i] * mileage[i] for i in range(len(trailers)))*cost_m + sum(trailers)*cost_t, GRB.MINIMIZE)
# Constrains
# Constrains 1 #trailers with goods that are required to keep shelves stocked
m.addConstr(trailers[0]+trailers[4]+trailers[8]+trailers[12], GRB.EQUAL,requirement[0])
m.addConstr(trailers[1]+trailers[5]+trailers[9]+trailers[13], GRB.EQUAL,requirement[1])
m.addConstr(trailers[2]+trailers[6]+trailers[10]+trailers[14], GRB.EQUAL,requirement[2])
m.addConstr(trailers[3]+trailers[7]+trailers[11]+trailers[15], GRB.EQUAL,requirement[3])

# Constrains 2 # goods that not exceed the trailer capacity of its DC'S
m.addConstr(trailers[0]+trailers[1]+trailers[2]+trailers[3], GRB.LESS_EQUAL,12000)
m.addConstr(trailers[4]+trailers[5]+trailers[6]+trailers[7], GRB.LESS_EQUAL,12000)
m.addConstr(trailers[8]+trailers[9]+trailers[10]+trailers[11], GRB.LESS_EQUAL,12000)
m.addConstr(trailers[12]+trailers[13]+trailers[14]+trailers[15], GRB.LESS_EQUAL,12000)

# Constrains 3 # Policy of serving each of its stores from one and only one DC
m.addConstr(g[0]+g[1]+g[2]+g[3], GRB.EQUAL,1)
m.addConstr(g[4]+g[5]+g[6]+g[7], GRB.EQUAL,1)
m.addConstr(g[8]+g[9]+g[10]+g[11], GRB.EQUAL,1)
m.addConstr(g[12]+g[13]+g[14]+g[15], GRB.EQUAL,1)

m.update()

# result
m.optimize()

