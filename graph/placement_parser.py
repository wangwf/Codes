result=[]
with open("placement.txt","r") as f:
    for line in f:
        result.append(line.split())

result

dirPath="/home/wenfeng/Venor/k-grid/hillclimb/calcserver/src/data-linkedin/"
def readFile(filename):
    import json
    with open(filename) as f:
        attribution= f.read()
        attribution=json.loads(attribution)
        attribution.pop("apiStandardProfileRequest",None)
        attribution.pop("id",None)
        attribution.pop("pictureUrl",None)

        res = attribution["firstName"]+attribution["lastName"] + ",\n"
        res += attribution['headline'].replace("&","-")+","
        location = attribution["location"]["name"]+","+ attribution["location"]["country"]["code"]
        res +="\n"+ str(location)

        return res
    return ""


n=len(result)
m=len(result[0])
def outputList():
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
    s1="""<?xml version="1.0" encoding="UTF-8"?> \n"""

#    s1 += """<graphml xmlns="http://graphml.graphdrawing.org/xmlns" 
#             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#             xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
#             http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">"""
    s1 += "<graphml>\n"

    s1 += """<key id="d0" for="node" attr.name="label" attr.type="string">   </key> \n"""
    s1 += """<graph id="G" edgedefault="undirected">\n"""


    outF.write(s1)
    for i in range(n):
        for j in range(m):
            nodeName = result[i][j]
            label= readFile(dirPath+result[i][j])

#            outF.write('<node id="'+result[i][j]+'"/>\n')
            outF.write('<node id="'+result[i][j]+'">\n')
            outF.write('  <data key="d0"> """' + str(label) + '"""</data>\n')
            outF.write('</node>\n')

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

    outF.write("</graph>")
    outF.write("</graphml>")
    outF.close()


outputgml("placement2.gml")

def outputgraphml(outfile="t.graphml"):
    outF = open(outfile,"w")
    s1="""<?xml version="1.0" encoding="UTF-8"?> \n"""

#    s1 += """<graphml xmlns="http://graphml.graphdrawing.org/xmlns" 
#             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#             xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
#             http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">"""
    s1 += "<graphml>\n"

    s1 += """<key id="d0" for="node" attr.name="label" attr.type="string">   </key> \n"""
    s1 += """<graph id="G" edgedefault="undirected">\n"""


    outF.write(s1)
    for i in range(n):
        for j in range(m):
            inode = 1+i*m+j
            nodeName = result[i][j]
            label= readFile(dirPath+result[i][j])

#            outF.write('<node id="'+result[i][j]+'"/>\n')
            outF.write('<node id="'+str(inode) +'">\n')
            outF.write('  <data key="d0"> ' + str(label) + '</data>\n')
            outF.write('</node>\n')

    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m
#            source  = result[i][j]
#            target1 = result[i1][j]
#            target2 = result[i2][j]
#            target3 = result[i][j1]
#            target4 = result[i][j2]
            source  = str(1 + i *m  + j)
            target1 = str(1 + i1 *m + j)
            target2 = str(1 + i2 *m + j)
            target3 = str(1 + i *m  +j1)
            target4 = str(1 + i *m  +j2)

            outF.write('<edge source="'+source+'" target="'+target1+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target2+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target3+'"/>\n')
            outF.write('<edge source="'+source+'" target="'+target4+'"/>\n')

    outF.write("</graph>")
    outF.write("</graphml>")
    outF.close()


outputgraphml("placement2.graphml")

def outputgraphml2(outfile="t.graphml"):

    import networkx as nx
    g = nx.Graph()

    nnodes = n*m
    g.add_nodes_from(range(1, nnodes+1))


    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m

            source  = (1 + i *m + j)
            target1 = (1 + i1*m + j)
            target2 = (1 + i2*m + j)
            target3 = (1 + i *m + j1)
            target4 = (1 + i *m + j2)

            g.node[source]['label'] = label= readFile(dirPath+result[i][j]) #result[i][j]
            g.add_edge( source, target1)
            g.add_edge( source, target2)
            g.add_edge( source, target3)
            g.add_edge( source, target4)



    nx.write_graphml(g, outfile)



outputgraphml2("placement2.graphml")

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
           # print readFile(dirPath+result[i][j])

    outF.write("*arcs\n")
    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m

            source  =  1+i*m+j
            target1 =  1+i1*m+j
            target2 =  1+i2*m+j
            target3 =  1+i*m+j1
            target4 =  1+i*m+j2

            outF.write( str(source)+' '+str(target1)+'\n')
            outF.write( str(source)+' '+str(target2)+'\n')
            outF.write( str(source)+' '+str(target3)+'\n')
            outF.write( str(source)+' '+str(target4)+'\n')

    outF.close()

dirPath="/home/wenfeng/Venor/k-grid/hillclimb/calcserver/src/data-linkedin/"
def outputNet2(outfile="t.net"):
    outF = open(outfile,"w")
    s1="*Vertices "+str(n*m) +"\n"
    outF.write(s1)
    nnodes=0
    for i in range(n):
        for j in range(m):
            nnodes = 1 + i*m+j
            nodeName = result[i][j]
            label= readFile(dirPath+result[i][j])
            outF.write( str(nnodes) + ' "' + nodeName + '"\n')
           # print readFile(dirPath+result[i][j])

    outF.write("*arcs\n")
    for i in range(n):
        for j in range(m):
            i1,i2= (i+1)%n, (i-1+n)%n
            j1,j2= (j+1)%m, (j-1+m)%m

            source  =  1+i*m+j
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
