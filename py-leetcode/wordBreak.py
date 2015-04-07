
def wordBreak(s, dict):
    segmented = [True]
    for i in range(len(s)):
        segmented.append(False)
        for j in range(i, -1, -1):
            if segmented[j] and s[j:i+1] in dict:
                segmented[i+1] = True
                break

    return segmented[len(s)]


def wordBreak(s, dict):
    """
    DP, A[0,..., n-1]

    """
    n = len(s)
    A = [False]*n

    i= n-1

    while i>= 0:
        if s[i:n] in dict:
            A[i] = True
        else:
            for j in range(i+1, n):
                if A[j] and a[i:j] in dict:
                    A[i] = True
                    break
        i -= 1
    return A[0]
