"""
Part 3. Memoizer

 a function that accepts a single-argument function f, and an integer k,
 and returns a function that behaves the same as f
except it caches the last k results of f.

Additional questions:
Q1: Can you describe the efficiency of the memoizer?
 A: for the below simple recursive fib-function, two previousl functions always cached, its complexity O(n) while the previousl one is approximately O(2^n)

Q2: What does your memoizer handle concurrent access?
 A: The SizedDict is implemented based on python's built-in dictionary,
    it is thread-safe.
"""

from limitedSizedDict import SizedDict

def memoizer(f,k):
    memo = SizedDict(k) #  k-sized dictionary
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

#
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


#fib = memoizer(fib,2)
print(fib(40))
