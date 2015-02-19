

def fib(n):
    parents, babies =(1,1)
    while babies<n:
        print 'This generation has {0} babies'.format(babies)
        parents, babies = (babies, parents+babies)
    return babies

#for i in range(2,100):    print fib(i)
fib(100)
