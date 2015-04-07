
#from sets import Set
graph = {'A': set(['B','C']),
         'B': set(['A','D','E']),
         'C': set(['A','F']),
         'D': set(['B']),
         'E': set(['B','F']),
         'F': set(['C','E'])
         }

def dfs(graph,start):
    visited=set()
    stack=[start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex]-visited)

    return visited




print dfs(graph,'A')

def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited=set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs_recursive(graph, next, visited)
    return visited




print dfs_recursive(graph,'A')



#dfs_path

def dfs_paths(graph, start, goal):
    stack = [(start,[start])]

    while stack:
        (vertex, path)=stack.pop()
        for next in graph[vertex] -set(path):
            if next == goal:
                yield path +[next]
            else:
                stack.append( (next, path+[next]))

'''           
def dfs_paths_recursive(graph, start, goal, path=None):
    if path is None:
        path=[start]
    if start == goal:
        yield path
    for next in graph[start]-set(path):
        yield from dfs_paths_recursive(graph, next, goal, path+[next])
'''
print list(dfs_paths(graph, "A","F"))
#print list(dfs_paths_recursive(graph, "A","F"))



#
#
def bfs(graph, start):
    visited, queue= set(), [start]
    while queue:
        vertex = queue.pop() #(0)
        if vertex not in visited:
            visited.add(vertex)
#            newnodes =[ n for n in graph[vertex] if n not in visited]
#            queue  += newnodes
            queue.extend(graph[vertex]-visited)
#            queue + graph[vertex]-visited
    return visited

print bfs(graph,'A')
