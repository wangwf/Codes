#!/usr/bin/env python

'''
'''


'''Depth First Traversal
start at node n
mark n as visited
for
'''
def DFS_nodes(graph, node, visited=[]):
    visited.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            DFS_nodes(graph, neighbor, visited)
    return visited


def DFS_edges(graph, node, visited=[], edges=[]):
    visited.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
 #       if (node,neighbor) not in edges and (neighbor,node) not in edges: #visited:
            edges.append((node, neighbor))
            DFS_edges(graph, neighbor, visited, edges)
#        else:
#             edges.append((node, neighbor))
    return edges

#networkx implement
def BFS_edges(graph, node):
    visited=set([node])
    queue=deque([(node, graph[node])])
    while queue:
        parent, children = queue[0]
        try:
            child = next(children)
            if child not in visited:
                yield parent, child
                visited.add(child)
                queue.append((child, neighbors(child)))
        except StopIteration:
            queue.popleft()

def test_graph():
    import networkx
    g = networkx.generators.small.krackhardt_kite_graph()
    print 'edges ', g.edges()
    e=networkx.traversal.dfs_edges(g)
    print 'edges ', list(e)
    e=networkx.traversal.bfs_edges(g)
    print 'edges ', list(e)

    #networkx.traversal.dfs_tree()
    visited=[]
#    print DFS_nodes(g, 0, visited)
    visited=[]
    edgs=[]
    print 'edges ',DFS_edges(g, 0)
    print g.edges()==DFS_edges(g, 0)

def generate_graph():
    import networkx
    g = networkx.generators.small.krackhardt_kite_graph()
    return g

def short_distance():
    from networkx import algorithms
    g=generate_graph()
    print algorithms.shortest_path(g,0,5)

    print algorithms.dijkstra_path(g,0,5)


def read_lj_friend(g, name):
    import urllib2
    import urllib
    response = urllib.urlopen('http://www.livejournal.com/misc/fdata.bml:user='+name)
    #
    for line in response.readline():
        if line.startswith("#"): continue
        #
        #the format is "< name " (incoming) or ">name" (outgoing)
        parts = line.split()
        print parts
        if len(parts)==0:continue
        #add edge to the network
        if parts[0]=='<':
            g.add_edge(parts[1], name)
        else:
            g.add_edge(name, parts[1])

import networkx
g=networkx.Graph()
read_lj_friend(g, 'valerois')
networkx.draw(g)

if __name__=='__main__':
    test_graph()


