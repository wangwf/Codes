#from pythonds.basic.stack import Stack

from stack import Stack

def parChecker(symbolString):
    s = Stack()
    balanced = True
    index =0
    while index<len(symbolString) and balanced:
        sym = symbolString[index]
        if sym =="(":
            s.push(sym)
        else:
            if s.isEmpty():
                balance =False
            else:
                s.pop()
        index += 1


    if s.isEmpty():
        return balanced
    else:
        return False

print(parChecker('((()))()'))
print(parChecker('(()'))


def matches(open, close):
    opens = "([{"
    closes = ")]}"
    return opens.index(open) == closes.index(close)

def parChecker2(symbolString):
    s=Stack()
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        if symbol in "([{":
            s.push(symbol)
        else:
            if s.isEmpty():
                balanced = False
            else:
                top = s.pop()
                if not matches(top, symbol):
                    balanced =False
        index = index +1

    if s.isEmpty():
        return balanced
    else:
        return False

print "test two parenthese"
print(parChecker2('{{([][])}()}'))
print(parChecker2('[{()]'))
