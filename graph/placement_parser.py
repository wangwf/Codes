result=[]
with open("placement.txt","r") as f:
    for line in f:
        result.append(line.split())

result


n=len(result)
m=len(result[0])
def output1():
    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m
#        print result[i][j], result[i1][j], result[i2][j],result[i][j1], result[i][j2]
#        print result[i][j], result[i2][j]
#        print result[i][j], result[i][j1]
#        print result[i][j], result[i][j2]
#        print 1+i*m+j, 1+i1*m+j, 1+i2*m+j, 1+i*m+j1, 1+i*m+j2
            print 1+i*m+j, 1+i1*m+j, 1.0
            print 1+i*m+j, 1+i2*m+j, 2.0
            print 1+i*m+j, 1+i*m+j1, 3.0
            print 1+i*m+j, 1+i*m+j2, 4.0


def outputgml(outfile="t.gml"):
    outF = open(outfile,"w")
    s1="""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
<graph id="G" edgedefault="undirected">\n"""

    outF.write(s1)
    for i in range(n):
        for j in range(m):
            outF.write('<node id="'+result[i][j]+'"/>\n')

    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m
            source=result[i][j]
            target1 = result[i1][j]
            target2 = result[i2][j]
            target3 = result[i][j1]
            target4 = result[i][j2]

            outF.write('<edge source="'+source+'" target="'+target1+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target2+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target3+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target4+'"/>\n')

    outF.close()


outputgml("placement2.gml")
outputgml("placement2.graphml")

#
#
#
def outputNet(outfile="t.net"):
    outF = open(outfile,"w")
    s1="*Vertices "+str(n*m) +"\n"
    outF.write(s1)
    nnodes=0
    for i in range(n):
        for j in range(m):
            nnodes = 1 + i*m+j
            outF.write( str(nnodes) + ' "' + result[i][j] + '"\n')

    outF.write("*arcs\n")
    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m

            source  = 1+i*m+j
            target1 =  1+i1*m+j 
            target2 =  1+i2*m+j 
            target3 =  1+i*m+j1 
            target4 =  1+i*m+j2 

            outF.write( str(source)+' '+str(target1)+'\n')
            outF.write( str(source)+' '+str(target2)+'\n')
            outF.write( str(source)+' '+str(target3)+'\n')
            outF.write( str(source)+' '+str(target4)+'\n')

    outF.close()


outputNet("placement2.net")
