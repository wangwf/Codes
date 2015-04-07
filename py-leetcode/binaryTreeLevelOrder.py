

def levelOrder(root):
    result =[]
    if not root: return result
    return dfs(root, 0, result)


def dfs(root, level, visited):
    if root if None: return []

    if level ==0 or level == len(visited):
        visited.append([root.val])
    else:
        visited[level].append(root.val)

    dfs(root.left, level+1, visited)
    dfs(root.right, level+1, visited)
    return visited


