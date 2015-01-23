
## data Cleaning

f  = open("learnDataSet.log", "r")
import csv

fo = open("output.txt","w")
writer = csv.writer(fo)

#line = f.readline()
#words = line.split(":") # ;

# Currently only extract a few features
fo.write("response-size,Runtime, Content-Length, request_method, Path\n")

l=0
for line in f:
    words = line.split(":")
    if len(words)<5:
        continue
    i=0
    record={}
    alist =[0,0,0,'','']
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
            ww = w.split(";")
            res['request_method']=ww[0].split("=")[1]
            alist[3]   = ww[0].split("=")[1]
            if ww[1].split("=")[0].lstrip()=="path":
                res['path']= ww[1].split("=")[1].split(",")[0]
                alist[4]   = ww[1].split("=")[1].split(",")[0]
                if l==0:
                    print "== ",w, "   ", ww[1].split("=")[0]
                    print words
                l +=1
        i += 1
    if alist[0]>0:
        writer.writerow(alist)
#        for item in alist:
#            fo.write("%s "%item)
#        fo.write("\n")
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


