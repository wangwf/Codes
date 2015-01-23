
## data Cleaning

f  = open("learnDataSet.log", "r")
fo = open("output.txt","w")

#line = f.readline()
#words = line.split(":") # ;

# Currently only extract a few features
fo.write("response-size Runtime Content-Length request_method Path")

l=0
for line in f:
    words = line.split(":")
    if len(words)<5:
        continue
    i=0
    record={}
    alist =[0,0,0,'','','']
    while i<len(words):
        w =words[i]
        if w.startswith("error"):  # or regext ?
            record['error'] = words[i].split(",")[1] # or words[i+1][0] ?

        elif w.startswith('response'):
            res={}
            res['response-size']=int( w[9:])
            alist[0] = int(w[9:])
        elif w.startswith("X-Runtime"):
            res['Runtime'] = float(words[i+1].split(",")[0])
            alist[1] =  float(words[i+1].split(",")[0])
        elif w.startswith("Content-Length"):
            res['Content-Length'] = int(words[i+1].split(",")[0])
            alist[2] =  int(words[i+1].split(",")[0])
        elif w.startswith("request_method"):
            res['request_method']=w.split(";")[0].split("=")[1]
            res['path']=w.split(";")[1].split("=")[1].split(",")[0]
            alist[3] = w.split(";")[0].split("=")[1]
            #alist[4] = w.split(";")[1].split("=")[1].split(",")[0]
        i += 1
    if alist[0]>0:
        for item in alist:
            fo.write("%s "%item)
        fo.write("\n")
#    record['response']=res        
#    fo.write(res)
    
           # print res
            #fo.write(res)

f.close()
fo.close()

print "res=\n"
print res
print "response "
print record


