
def read_lj_friend(g, name):
    import urllib2, urllib
    response = urllib.urlopen('http://www.livejournal.com/misc/fdata.bml?user='+name)
    #
#    for line in response.readline():
    for line in response:
        if line.startswith("#"): continue
        #
        #the format is "< name " (incoming) or ">name" (outgoing)
        parts = line.split()
        print parts
        if len(parts)<=1:continue
        #add edge to the network
        if parts[0]=='<':
            g.add_edge(parts[1], name)
        else:
            g.add_edge(name, parts[1])

import networkx
g=networkx.Graph()
read_lj_friend(g, 'valerois')
networkx.draw(g)
networkx.draw_random(g)
import matplotlib.pyplot as plt
plt.show()
