
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

import copy
def helper(root, sum, res, path):

    if not root:
        return

    path.append(root.val)

    if not root.right and not root.left:
        if root.val == sum:
            res.append(copy.deepcopy(path))
            print res

    if root.left:
        helper(root.left, sum - root.val, res, path)

    if root.right:
        helper(root.right, sum - root.val, res, path)

    path.pop()

def pathSum(root, sum):
    res=[]
    if not root:
        return res

    path =[]
    helper(root, sum, res, path)

    return res


root=TreeNode(1)

print pathSum(root, 1)
