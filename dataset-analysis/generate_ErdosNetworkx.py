import networkx as nx
import random
import matplotlib.pyplot as plt 

G= nx.erdos_renyi_graph(1573,0.023)
f = open("erdos_renyi_output", "w")
for line in nx.generate_adjlist(G):
    splittedLine=line.split(" ")
    for x in range(1,len(splittedLine)):
        strToPrint=str(int(splittedLine[0])+1)+" "+str(int(splittedLine[x])+1)+" "+str(random.randint(1,555555))+"\n"
        f.write(strToPrint)
f.close()
nx.draw(G, with_labels=True) 
plt.show() 