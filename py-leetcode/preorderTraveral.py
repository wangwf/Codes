


class TreeNode:
    def __init__(self, x):
        self.val =x 
        self.left = None
        self.right = None

    def preorderTraversal(self, root):
        res = []
        self.help(root, res)
        return res

    def helper(self, root, res):
        if root is None:
            return
        res.append(root.val)
        self.helper(root.left, res)
        self.helper(root.right, res)


    def preorder_stack(self, root):
        res=[]
        if not root:
            return

        res =[]
        stack=[root]

        while stack:
            top = stack.top()
            res.append(top.val)
            if top.right:
                stack.append(top.right)
            if top.left:
                stack.append(top.left)

        return res

