
'''
Generate the top 10 3-grams for the article
 http://en.wikipedia.org/wiki/N-gram
'''

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

#downloadWikiPage("N-gram", "ngram.txt")


#
# ngram from alist
#
def ngrams(alist, n):
    return zip(*[alist[i:] for i in range(n)])

# Markove model
def markove(alist, n):
    keys = ngrams(alist, n)
    markovM ={}
    for k in keys:
        markovM[k] = (markovM.get(k) or 0) +1
    return markovM



if __name__ =="__main__":

    topic, inFile ="N-gram", "ngram.txt"
    # downloading data
    import os
    if not os.path.exists(inFile):
        downloadWikiPage(topic, inFile)

    # read data
    with open("ngram.txt","r") as f:
        content=f.read()

    # tokenize using NLTK
    import nltk
    words = nltk.word_tokenize(content)

    # Bag-Of-Words model for n-gram
    bow = markove(words, 3) # bag of word

    # sorted by dictionary value
    import operator
    sorted_bow = sorted(bow.items(), key=operator.itemgetter(1))

    # print the top-10 3-gramma
    print sorted_bow[-1:-10:-1]

