

def getBalanced(root):
    if not root:
        return 0, True

    left, lb = getBalanced(root.left)
    if not lb:
        return left+1, lb
    right, rb = getBalanced(root.right)
    if not rb:
        return right+1, rb

    if (abs(left - right))>1:
        return 1 + max(left, right), False
    return 1 + max(left, right), True

def isBalanced(root):
    depth, balanced = getBalanced(root)
    return balanced

        
