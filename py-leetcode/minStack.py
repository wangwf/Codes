class MinStack:
    # @param x, an integer
    # @return an integer
    def __init__(self):
        self.stack  = []
        self.mini = None

    def push(self, x):
        self.stack.append(x)

        if self.mini:
            if self.mini >x:
                self.mini = x
        else:
            self.mini=x
        return x

    # @return nothing
    def pop(self):
        top=self.stack.pop()

        if self.mini == top:
            if self.stack:
                self.mini = min(self.stack)
            else:
                self.mini = None
        return top

    # @return an integer
    def top(self):
        return self.stack[-1]


    # @return an integer
    def getMin(self):
#        print self.minIdx
        return self.mini



test = MinStack()
test.push(2)
test.push(0)
test.push(3)
test.push(0)
test.pop()
test.getMin()
test.pop()
test.getMin()
test.pop()
test.getMin()

