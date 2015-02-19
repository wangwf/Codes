
'''
  N-Gram generator
'''
#
# the obvious way
def find_bigrams(inputList):
    bigrams=[]
    for i in range(len(inputList)-1):
        bigramst.append( (inputList[i], inputList[i+1]))
    return bigrams


# using slicing and zipping
# zip() takes a list of iterables and constructs a new list of tuples
def bigrams2(alist):
    return zip(alist, alist[1:])


#
# List comprehension 
def ngrams(alist, n):
    return zip(*[alist[i:] for i in range(n)])


if __name__ == "__main__":
    import re
    s =" Stack Overflow is a question and answer site for professional and enthusiast programmers. It's 100% free, no registration required."
    words = s.strip(" ").split(" ")

    print ngrams(words, 4)
