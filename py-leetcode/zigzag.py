'''
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:

string convert(string text, int nRows);
convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".
'''

def convert(s, nRows):
    if nRows==1 or len(s)<nRows:
        return s

    ret=['']*nRows
    level =0
    countdown= False
    for i in range(len(s)):
        ret[level] += s[i]
        if level ==0 or level==nRows -1:
            countdown = not countdown
        if countdown:
            level += 1
        else:
            level -= 1

    return ''.join(ret)


s="PAYPALISHIRING" 
s2="PAHNAPLSIIGYIR"
print convert(s,3) ==s2
