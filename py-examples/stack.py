class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items ==[]

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) -1]

    def size(self):
        return len(self.items)

#from pyhonds.basic.stack import Stack

def test():
    s = Stack()
    print(s.isEmpty())
    s.push(4)
    s.push('dog')
    print(s.peek())
    s.push(True)
    print(s.size())
    print(s.isEmpty())
    s.push(8.4)
    print(s.pop())
    print(s.pop())
    print(s.size())

    m = Stack()
    m.push('x')
    m.push('y')
    m.push('z')
    while not m.isEmpty():
        m.pop()
#   m.pop()

