
def longestCommonPrefix(strs):
    is strs==[]: return ""

    rightMost = len(strs[0])
    for i in range(1, len(strs)):
        if rightMost>len(strs[i]):
            rightMost = len(strs[i])
        j=0
        while j<rightMost:
            if strs[0][j] != strs[i][j]:
                rightMost =j
            j +=1
    return strs[0][:rightMost]
