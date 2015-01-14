
'''

'''


def atoi(str):
    MAXINT = 2**31 -1
    MININT = -2**31

    if str=="": return 0
    idx =0
    while str[idx]==' ': idx +=1

    sign =1
    if str[idx] == "-":
        idx +=1
        sign = -1
    elif str[idx] == "+":
        idx += 1

    res =0
    while idx<len(str):
        if str[idx].isdigit():
            res = res*10 + ord(str[idx]) - ord('0')
            if sign*res > MAXINT:
                return MAXINT
            elif sign*res < MININT:
                return MININT
        else:
            break
        idx += 1

    return sign*res

print atoi("321")
