"""Part 3. Memoizer

Write a function that accepts a single-argument function f, and an integer k, and returns a function that behaves the same as f except it caches the last k results of f.

For instance, if memoize is the function we’re after, and let mem_f = memoize(f, 2), then
mem_f(arg1) → f(arg1) is computed and cached
mem_f(arg1) → f(arg1) is returned from cache
mem_f(arg2) → f(arg2) is computed and cached
mem_f(arg3) → f(arg3) is computed and cached, and f(arg1) is evicted

Additional questions:
Can you describe the efficiency of the memoizer?
What does your memoizer handle concurrent access?



"""

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

#fib = memoize(fib)

print(fib(40))
