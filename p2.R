library(optrees)
nodes <- 1:8
arcs <- matrix(c(1,2,20, 1,3,15, 2,5,15, 2,4,10, 3,4,13, 3,7,10, 3,6,15,
               4,5,10, 4,7,12, 4,3,13, 5,6,7, 5,8,10, 5,2,15,
               6,8,8, 6,7,8, 7,8,10, 7,6,8), byrow = T, ncol=3)
arcs
maxFlowFordFulkerson(nodes = nodes, arcs = arcs, source.node = 1, sink.node = 8)
# Same answer from Excel Solver max.flow is 28

maxflowk <- c()
for (k in 1:10){
  arcs <- matrix(c(1,2,20*k, 1,3,15*k, 2,5,15, 2,4,10, 3,4,13, 3,7,10, 3,6,15,
                   4,5,10, 4,7,12, 4,3,13, 5,6,7, 5,8,10*k, 5,2,15,
                   6,8,8*k, 6,7,8, 7,8,10*k, 7,6,8), byrow = T, ncol=3)
  graph <- graph_from_data_frame(arcs[,1:2])
  maxflowk[k] <- graph.maxflow(graph,source = 1, target = 8, capacity=arcs[,3])$value
}
#graph
maxflowk

#The limit max flow for the graph is 62, when k=3
# Increasing the capacity of all arcs leading out of tank 1 and all arcs leading into the tank 8
# will allow it to double the maximum flow 62 is larger than 28*2=56
