# reverse string
#  s = "The sky is blue"
# return "blue is sky the"
def reverseWords(s):
    #s = " ".join(s.split()[::-1])
    s = s.split() # split the sentence in list of words
    s = s[::-1]
    s = " ".join(s)
    return s
