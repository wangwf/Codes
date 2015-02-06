


'''
#The log files follows the pattern
   n1:length-n1-string:1#]}:n2:length-n2-string:1#]}... nn:length-nn-string:1#]}
'''
def checkPattern(filename):

    with open(filename) as f:
        #f = open(filename,"r")
        text = f.read()
    start = 0  # n = text[nfirst:nend]
    end   = 0
    while end > -1:
        end  = text.find("1#]}", start)
        #print start,end
        if end==-1:
            if start != len(text):
                print "Mismatch ending part."
            break

        n1end = text.find(":",start)
        if n1end== -1:
            print " Can't find the first length ",n1end, start, end
            continue

        n1 = text[start:n1end]
        #print n1
        if not n1.isdigit():
            print "n1 is not digit ",n1
            continue
        n1 = int(n1)
        if n1 -(end- n1end+2) !=0:
            print "Length Pattern break!", n1,end- n1end+2, end, n1end

        start = end+4

    print filename,": pattern check OK!"



'''

'''
def replace_between(text, begin, end, alternative=''):
    middle = text.split(begin, 1)[1].split(end, 1)[0]
    return text.replace(middle, alternative)

#
# only skip all HTML 
def skipHTML(infile, beginPattern="<!DOCTYPE html>", endPattern ="</html>"):
    with open(infile,"r") as f:
        text =f.read()

    print "Origin file size ", len(text)
    first,end = 0,0
    while end>-1:
        first= text.find(beginPattern) #
        end  = text.find(endPattern,first)
        #print first, end
        middle=text[first:end+7]
        text=text.replace(middle,"")
        '''
        if first>-1:
            if end==-1:
                print "Wrong HTML pattern! Please check."
                return
            nl  += end-first+7
            newtext = newtext[:first]+newtext[end+7:]
            print first, end, nl, len(newtext)
        '''
    print "After cleaning ",len(text)
    return text



#skip all content: HTML, javascript
def skipAllContents(infile, beginPattern="content,", endPattern="cert,0"):
    with open(infile,"r") as f:
        text =f.read()

    print "Origin file size ", len(text)
    first,end = 0,0
    while first>-1:
        first= text.find(beginPattern,first+1) #
        #end  = text.find(endPattern,first) #

        ncolon = text.find(":",first)
        if ncolon ==-1:
            continue
        ncontent = text[first+len(beginPattern):ncolon ]
        if not ncontent.isdigit():
            print "Warning non digit"
            continue
        ncontent = int(ncontent)

        #print first, end
        middle=text[ncolon+1: ncolon+ ncontent+1]
        print  text[first+len(beginPattern):ncolon ], ncontent
        text=text.replace(middle,"")

    print "After cleaning ",len(text)
    return text

#newtext = skipHTML(flearn)  #replace_between(text,"<!DOCTYPE html>", "</html>", "")
#len(newtext), newtext.find("<!DOCTYPE html>")


def keyValuePairCheck(infile, features, option=1):
    ''' data formate check
      :field,n:nextString   Does n== len(nextString) ?
    '''
    if option==1:
        with open(infile, "r") as f:
            text = f.read()
    elif option==2:
#        text = skipHTML(infile)
        text = skipAllContents(infile)

    ntrue =0
    nfalse=0
    nfeatures =0
    nwarnings =0
    # Global check pattern
    words = text.split(":")
    print len(words),len(text)
    for i in range(len(words)):
        if words[i].find(",")<0:
                continue
        key,n = words[i].split(",",1)  # only use the first coma
#        key= ww[0]
#        n  = ww[1]
        if key in features:
            nfeatures +=1
            '''
            if not n.isdigit():
                print "Warning n is not digit",words[i]
                nwarns +=1
            '''
        else:
            if  n.isdigit():
                print words[i],"  ", words[i+1][:int(n)]
                if int(n) != len(words[i+1][:int(n)]):
                    print "Waring length not equal",words[i],words[i+1]
                    nwarnings +=1
            else:
                #print "n is not digit",n, words[i]
                pass

    print "\n"
    print "Number of good Pattern ", ntrue
    print "Number of good features ", nfeatures
    print "Number of bad  Pattern ", nfalse
    print "Number of Warnings ", nwarnings

    return



#
#  Below recursive Parsing doesn't work well yet, need to be check
#
def recursiveParsing(text):
    if text=="":
        return text

    words=text.split(":",1)
    if len(words)==1:
        return text

    w1 = words[0]
    w2 = words[1]

    if w1.isdigit():
        #subtext = word[1][:int(v)+1]
        recursiveParsing(w2[:int(w1)+1])
        recursiveParsing(w2[int(w1)+1:])
    else:
        if w1.find(",")>-1:
            key,v = w1.split(",",1)
            print key,v
            if v.isdigit():
                value = w2[:int(v)+1]
                print {key:v},value,
                if value.find(":")>-1:
                    recursiveParsing(value)
                else:
                    print {key:recursiveParsing(value)}
                recursiveParsing(w2[int(v)+1:])
            else:
                print {key:v}



#text = skipAllContents(flearn)
#recursiveParsing(text)
#text
