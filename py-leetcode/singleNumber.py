"""
Given an array of integer, every element apprears twice except for one, 
find the single one.
"""

def singleNumber(A):
    if len(A)<1:
        return None

    res=A[0]
    for i in A[1:]:
        res = res^A[i]

    return res
