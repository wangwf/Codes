#
# PalindromeChecker

from deque import Deque

def palchecker(aString):
    chardeque = Deque()

    for ch in aString:
        chardeque.addRear(ch)

    stillEqual = True

    while chardeque.size() >1 and stillEqual:
        first = chardeque.removeFront()
        last = chardeque.removeRear()
        if first != last:
            stillEqual = False

    return stillEqual


print(palchecker("lsdkjfskf"))
print(palchecker("radar"))


def palchecker2(aString):
    isEqual =True
    l = len(aString)
    i = 0
    while i<= l/2 and isEqual:
        if aString[i] != aString[l-1-i]:
            isEqual =False
        i +=1

    return isEqual


print(palchecker("lsdkjfskf"))
print(palchecker("radar"))
