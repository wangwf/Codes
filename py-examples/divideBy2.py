
from stack import Stack

def divideBy2(decNumber):
    remstack = Stack()

    while decNumber >0:
        rem = decNumber%2
        decNumber = decNumber//2
        remstack.push(rem)

    binString = ""
    while not remstack.isEmpty():
        binString = binString + str(remstack.pop())

    return binString

print(divideBy2(42))


def baseConverter(decNumber, base):
    digits ="0123456789ABCDF"
    remstack = Stack()
    while decNumber >0:
        rem = decNumber %base
        decNumber = decNumber//base
        remstack.push(rem)

    newString =""
    while not remstack.isEmpty():
        newString = newString + digits[remstack.pop()]

    return newString

print(baseConverter(25, 2))
print(baseConverter(25, 8))
print(baseConverter(256, 16))

