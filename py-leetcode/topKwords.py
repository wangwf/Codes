"""
find the top k most frequency words in a string
"""

def topK(s, k):
    # words tokenize
    words = s.split(" ")
    
    # word counting
    wordCount = {}
    for w in words:
        wordCount[w] = (wordCount.get(w) or 0) + 1

    res=[]
    i =0
    for w in wordCount:
        c = wordCount[w]
        if i<k:
            res.append( (w,c))
        else:
            minCount = min(res, key= lambda item:item[1])
            if c>minCount[1]:
                res.remove( minCount)
                res.append( (w,c))
        i +=1

#    print res
    return zip(*res)[0]
        

s1 = "this is a string a string this is string string string string this this"

print topK(s1,2)
