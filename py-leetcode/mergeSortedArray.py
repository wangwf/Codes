
'''
 Given two sorted integer arrays A and B, merge B into A as one sorted array.
You may assume that A has enough space (size that is greater or equal to m + n) to hold additional elements from B. The number of elements initialized in A and B are m and n respectively.
'''

def merge(A, m, B, n):
    # @param A  a list of integers
    # @param m  an integer, length of A
    # @param B  a list of integers
    # @param n  an integer, length of B
    # @return nothing
    k = m + n -1
    i = m -1
    j = n -1
    while i>=0 and j>=0:
        if A[i] >=B[j]:
            A[k] = A[i]
            i -= 1
        else:
            A[k] = B[j]
            j -= 1
        k -=1
    while j>=0:
        A[k] = B[j]
        k -=1
        j -=1
    return A
