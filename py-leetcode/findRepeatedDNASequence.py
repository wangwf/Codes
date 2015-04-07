
"""
All DNA is composed of a series of nucleotides abbreviated as A, C, G, and T, for example: "ACGAATTCCG". When studying DNA, it is sometimes useful to identify repeated sequences within the DNA.

Write a function to find all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule.

For example,

Given s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",

Return:
["AAAAACCCCC", "CCCCCAAAAA"].
"""

def findRepeat(s):

    n = len(s)
    res = []

    dic = {}
    for i in range(n -9):
        dna = s[i:i+10]
        dic[dna] = (dic.get(dna) or 0)  + 1

    for k in dic:
        if dic[k] > 1:
            res.append(k)

    return res
