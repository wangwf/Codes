
def swap(A, m, n):
    temp = A[m]
    A[m] = A[n]
    A[n] = temp

def sortColors(A):

    n = len(A)
    r, w, b = 0, 0, n-1
    while w<=b:
        if A[w] == 0:
            swqp(A, w, r)
            w, r = w+1, r+1
        elif A[w] == 2:
            swap(A, b, w)
            b = b-1
        else:
            w -= 1

