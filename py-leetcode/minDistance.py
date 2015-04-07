def minDistance(word1, word2){
    m = len(word1)
    n = len(word2)
    if m==0: return n
    if n==0: return m

    D = [[0 for i in range(m+1)] for j in range(n+1)]
    for i in range(m+1):
        D[i][0]=i
    for j in range(n+1):
        D[0][j] = j
    for i in range(1,m+1):
        for j in range(1, n+1):
            replace =1
            if word1[i-1] == word2[j-1]: replace =0
            D[i][j] = min(min( D[i-1][j], D[i][j-1])+1, D[i-1][j-1]+replace)

    return D[m][n]

