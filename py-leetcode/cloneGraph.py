

class UndirectedGraphNode:
    def __init__(self, x):
        self.label =x
        self.neighborx =[]


Class Solution:
    def cloneGraph(self, node):
        if not node:
            return None
        visited ={}
        return self.dfsClone(node, visited)


    def dfsClone(self,root, visited):
        if not root: return None
        rootCopy = UndirectedGraphNode(root.label)
        visited[root] = rootCopy

        for n in root.neighbors:
            if n in visited:
                visited[root].neighbors.append(visited[n])
            else:
                visited[root].neighbors.append(self.dfsClone(n, visited))

        return rootCopy
