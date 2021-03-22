import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt


# BA algo functions
nodes_probs = []
nodes_degrees=[]

def get_rand_prob_node():
    #when we add new nodes to the graph, we take into account 
    print (nodes_probs,sum(nodes_probs))
    random_probability_node = np.random.choice(G.nodes(),p=nodes_probs)
    return random_probability_node

def add_edge():
        #if there are no edges to the node, we assign 0
    if len(G.edges()) == 0:
        random_probability_node = 0
    else:
        #else get a node random, but with custom probability
        random_probability_node = get_rand_prob_node()
        
    new_edge = (random_probability_node, new_node)

    #if edge already exists, retry, else add the edge
    if new_edge in G.edges():
         add_edge()
    else:
        nodes_degrees[random_probability_node]+=1
        nodes_probs[random_probability_node]= nodes_degrees[random_probability_node] / (2 * len(G.edges()))

        G.add_edge(new_node, random_probability_node)

init_nodes=18
final_nodes=1573
#this would be the median number of edges/node
m_parameter=18

#create the initial "group" of hub nodes (the important ones, that will have multiple edges to them)
G = nx.complete_graph(init_nodes)

count = 0
new_node = init_nodes

#we add node_probs initial nodes
for node in G.nodes():
    node_degree = G.degree(node)
    # node_probability = node_degree / (2 * len(G.edges()))
    nodes_degrees.append(node_degree)
    nodes_probs.append(node_degree / (2 * len(G.edges())))

#after we create initial complete nodes, we start to add the rest of the nodes and edges
for f in range(final_nodes - init_nodes):
    print (count)
    nodes_probs.append(0)
    nodes_degrees.append(0)
    G.add_node(init_nodes + count)
    count += 1
    for e in range(0, m_parameter):
        add_edge()
    new_node += 1



f = open("barbase_albert_output", "w")
for line in nx.generate_adjlist(G):
    splittedLine=line.split(" ")
    for x in range(1,len(splittedLine)):
        strToPrint=str(int(splittedLine[0])+1)+" "+str(int(splittedLine[x])+1)+" "+str(random.randint(1,555555))+"\n"
        f.write(strToPrint)
f.close()
