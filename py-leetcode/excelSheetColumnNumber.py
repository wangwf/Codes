'''
Related to question Excel Sheet Column Title

Given a column title as appear in an Excel sheet, return its corresponding column number.

For example:

    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28 

'''

def titleToNumber1(s):
    n = len(s)
    res=0
    for i in range(n):
        res = res*26 + ord(s[i]) - ord("A") +1
    return res

def titleToNumber(s):
    number =0
    for i in range(len(s)):
        n= ord(s[i]) - ord("A")+1
        if i < len(s)-1:
            number += pow(26, (len(s)-1-i))*n
            print "  ",number
        else:
            number += n
            print "  ",number

    return number


print titleToNumber("A")
print titleToNumber("Z")
print titleToNumber("AA")
print titleToNumber("AB")
print titleToNumber("BB")
print titleToNumber("AAA")


def convertToTitle(num):
    if num==0: return ""
    return convertToTitle( (num-1)/26) + chr( (num-1)%26 + ord("A"))

def convertToTitle(num):
    res =""
    while num>0:
        res += chr( (num-1)%26 + ord("A"))
        num = (num-1)/26

    return res[::-1]
