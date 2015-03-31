"""
Part 3. Memoizer

 a function that accepts a single-argument function f, and an integer k,
 and returns a function that behaves the same as f
except it caches the last k results of f.

Additional questions:
Can you describe the efficiency of the memoizer?
What does your memoizer handle concurrent access?
"""

from limitedSizedDict import SizedDict

def memoize(f,k):
    memo = SizedDict(k) #{}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

#@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
#        return memoize(fib(n-1),2) + memoize(fib(n-2),2)

fib = memoize(fib,2)
print(fib(40))
