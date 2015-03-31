"""
Generate the top 10 3-grams for the article
 http://en.wikipedia.org/wiki/N-gram

Methods:
 1.) use wikipedia package to download and parse wikipedia pages
 2.) defining ngram-model
 3.) remove punctuations
"""

#
# Wikipedia, a python library to access and parse data from wikipedia
#
def downloadWikiPage(topic, outfile):
    import wikipedia
    # print wikipedia.summary("Wikipedia")
    # wikipedia.search("N-gram")
    wiki  = wikipedia.page(topic)
    print wiki.title,wiki.url
    content = wiki.content.encode("ascii","ignore")
    with open(outfile, "w") as f:
        f.write( str(content))


#
# ngram from a list
#
def ngrams(alist, n):
    return zip(*[alist[i:] for i in range(n)])

#
# Words counting
#
def ngramsCount(alist, n):
    keys = ngrams(alist, n)
    ngramsC ={}
    for k in keys:
        ngramsC[k] = (ngramsC.get(k) or 0) +1
    return ngramsC



if __name__ =="__main__":

    topic, inFile ="N-gram", "ngram.txt"
    # downloading data
    import os
    if not os.path.exists(inFile):
        downloadWikiPage(topic, inFile)

    # loading data
    with open("ngram.txt","r") as f:
        content=f.read()

    # tokenize using NLTK
    import nltk
    words = nltk.word_tokenize(content)

    # remove punctuation
    import string
    punctuations = list(string.punctuation)
    punctuations.append("''")
    words = [i for i in words if i not in punctuations]

    words = [i.strip("".join(punctuations)) for i in words if i not in punctuations]

    words = [i for i in words if i != '']

    # Bag-Of-Words model for n-gram
    bow = ngramsCount(words, 3) # bag of word

    # sorted by dictionary value
    import operator
    sorted_bow = sorted(bow.items(), key=operator.itemgetter(1))

    # print the top-10 3-gramma
    for x in sorted_bow[-1:-10:-1]:
        print x

