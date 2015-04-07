

def pow1(x, n):
    if n==0:
        return 1

    half = pow(x, n/2)
    if n%2 == 0:
        return half*half
    else:
        if n>0:
            return x*half*half
        else:
            return 1/x*half*half


def pow(x, n):
    if n == 0: return 1

    res= pow(x*x, int(float(n)/2))

    return res if n%2 ==0 else res* (x if n>0 else 1/x) 
pow(34.005, -3)

