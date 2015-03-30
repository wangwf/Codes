
'''
Generate the top 10 3-grams for the article
 http://en.wikipedia.org/wiki/N-gram
'''

def downloadPage(url, outfile):
    import urllib2
    response = urllib2.urlopen(url)
    html = response.read()
    with open(outfile, "w") as f:
        f.write(html)


downloadPage("http://en.wikipedia.org/wiki/N-gram", "ngram.html")


#
# ngram from alist
#
def ngram(alist, n):
    return zip(*[alist[i:] for i in range(n)])

# Markove model
def markove(alist, n):
    keys = ngrams(alist, n)
    markovM ={}
    for k in keys:
        markovM[k] = (markovM.get(k) or 0) +1
    return markovM
