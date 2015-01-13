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
