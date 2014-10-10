
def listSum(numlist):
    theSum = 0
    for num in numlist:
        theSum = theSum+num
    return theSum


def listSum2(numlist):
    if len(numlist) ==1:
        return numlist[0]
    else:
        return numlist[0] + listSum(numlist[1:])

print(listSum2([1,3,5,7,9]))
