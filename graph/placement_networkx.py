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

            g.node[source]['id'] = result[i][j]
            g.node[source]['label']=readFile(dirPath+result[i][j]) #result[i][j]
#            g.node[source]['label'] = label= readFile(dirPath+result[i][j]) #result[i][j]
            g.add_edge( source, target1)
            g.add_edge( source, target2)
            g.add_edge( source, target3)
            g.add_edge( source, target4)



    nx.write_graphml(g, outfile)



outputgraphml2("placement2.graphml")

