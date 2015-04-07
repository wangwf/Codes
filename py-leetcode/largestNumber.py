'''
Given a list of non negative integers, arrange them such that they form the largest number.

For example, given [3, 30, 34, 5, 9], the largest formed number is 9534330.

Note: The result may be very large, so you need to return a string instead of an integer.
'''

def compare(a,b):
    return [1,-1][a+b>b+a]

def largestNumber(nums):
    nums =sorted( [str(x) for x in nums], cmp=compare)
    ans = ''.join(nums).lstrip('0')

    return ans or '0'

