import networkx as nx
g= nx.Graph()

#Nodes
g.add_node(1)
g.add_node("a")

#add a list of nodes
g.add_nodes_from([2,3,4])

#add attribute to node
g.node[1]["type"]='number'
g.node[1]["label"]='xyz'

print g.node[1]
print g.nodes()
print len(g)


#Edges
g.add_edge(1,2)
g.add_edges_from([(1,4), (1,3)])
g[1][2]['weight']=2.3

print g[1][2]
print g.edges()
print g.number_of_edges()

nx.write_graphml(g, "tt.graphml")

# Generating Erdo Renyi Graph
er = nx.erdos_renyi_graph(100, 0.15)
nx.draw(er)

