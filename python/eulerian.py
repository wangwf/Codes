from collections import defaultdict
from random import choice
def find_eulerian_tour(graph):
    # nodes: dictionary of edges to travel in the form {node: list of nodes connected to that node}
    nodes = defaultdict(list)
    for k,l in graph:
        nodes[k].append(l)
        nodes[l].append(k)

    # pick a random node to begin the path
    node = choice(nodes.keys())
    path = [node]

    print nodes,type(nodes)
    print node,type(node)
    print 'path',path,type(path)
    # traverse the graph. remove used edges as you go
    while len(nodes[node]) > 0 :
        after = nodes[node].pop()
        nodes[after].remove(node)      
        path.append(after)
        node = after

    # find nodes in our path that still have unused edges
    for node, node_list in nodes.iteritems():
        if node in path and len(node_list)>0:

            # insert "detour" into our path. as before, remove edges as you go
            index = path.index(node)
            while len(nodes[node]) > 0 :
                after = nodes[node].pop()
                nodes[after].remove(node)
                index+=1
                path.insert(index,after)
                node = after

    return path


graph=[(1, 2), (2, 3), (3, 1)]
print find_eulerian_tour(graph)
graph=[(0, 1), (1, 5), (1, 7), (4, 5),(4, 8), (1, 6), (3, 7), (5, 9),(2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
print find_eulerian_tour(graph)
