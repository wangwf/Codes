
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def isSymmetric(self, root):
        if not root:
            return True
        return self.isParity(root.left, root.right)

    def isParity(self, left, right):
        if not left and not right:
            return True
        elif not left or not right:
            return False

        if left.val != right.val:
            return False

        if self.isParity(left.left, right.right):
            return self.isParity(left.right, right.left)

        return False
