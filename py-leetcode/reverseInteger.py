
'''
Reverse digits of an integer.

Example1: x = 123, return 321
Example2: x = -123, return -321

click to show spoilers.

Have you thought about this?
Here are some good questions to ask before coding. Bonus points for you if you have already thought through this!

If the integer's last digit is 0, what should the output be? ie, cases such as 10, 100.

Did you notice that the reversed integer might overflow? Assume the input is a 32-bit integer, then the reverse of 1000000003 overflows. How should you handle such cases?

For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.

Update (2014-11-10):
Test cases had been added to test the overflow behavior.
'''
def reverse(x):
    MAXINT = 2**31
    res = 0
    isNeg = x<0
    x=abs(x)

    while x:
        res= res*10 + x%10
        x=x/10

    if ret >MAXINT: return 0
    if isNeg:
        res *= -1

    return res

def reverse2(x):
    MAXINT = 2**31
    isNeg =False
    if x<0: 
        isNeg = True
        x = -x

    x = int(str(x)[::-1])
    if x>MAXINT: return 0
    if isNeg: x = -x
    return x
print reverse(123)
print reverse(-231)
print reverse(1534236469)
