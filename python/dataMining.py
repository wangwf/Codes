#!/usr/bin/env python
#
# Data Mining: Discovering and Visualizing Patterns with Python
#
#http://refcardz.dzone.com/refcardz/data-mining-discovering-and#refcard-download-social-buttons-display
#

import urllib2
url = 'http://aima.cs.berkeley.edu/data/iris.csv'
u = urllib2.urlopen(url)
localFile = open('iris.csv', 'w')
localFile.write(u.read())
localFile.close()


from numpy import genfromtxt, zeros
# read the first 4 columns
data = genfromtxt('iris.csv',delimiter=',',usecols=(0,1,2,3)) 
# read the fifth column
target = genfromtxt('iris.csv',delimiter=',',usecols=(4),dtype=str) 


print data.shape
print target.shape

print set(target) # build a collection of unique elements
set(['setosa', 'versicolor', 'virginica'])

from pylab import plot,show
def test_plot():
    from pylab import plot, show
    plot(data[target=='setosa',0],data[target=='setosa',2],'bo')
    plot(data[target=='versicolor',0],data[target=='versicolor',2],'ro')
    plot(data[target=='virginica',0],data[target=='virginica',2],'go')
    show()

def test_subplot():
    from pylab import figure, subplot, hist, xlim, show
    xmin = min(data[:,0])
    xmax = max(data[:,0])
    figure()
    subplot(411) # distribution of the setosa class (1st, on the top)
    hist(data[target=='setosa',0],color='b',alpha=.7)
    xlim(xmin,xmax)
    subplot(412) # distribution of the versicolor class (2nd)
    hist(data[target=='versicolor',0],color='r',alpha=.7)
    xlim(xmin,xmax)
    subplot(413) # distribution of the virginica class (3rd)
    hist(data[target=='virginica',0],color='g',alpha=.7)
    xlim(xmin,xmax)
    subplot(414) # global histogram (4th, on the bottom)
    hist(data[:,0],color='y',alpha=.7)
    xlim(xmin,xmax)
    show()


def test_classification():
    t = zeros(len(target))
    t[target == 'setosa'] = 1
    t[target == 'versicolor'] = 2
    t[target == 'virginica'] = 3

    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(data,t) # training on the iris dataset

    print classifier.predict(data[0])
    print t[0]


    from sklearn import cross_validation
    train, test, t_train, t_test = cross_validation.train_test_split(data, t, test_size=0.4, random_state=0)

    classifier.fit(train,t_train) # train
    print classifier.score(test,t_test) # test

    from sklearn.metrics import confusion_matrix
    print confusion_matrix(classifier.predict(test),t_test)

    from sklearn.metrics import classification_report
    print classification_report(classifier.predict(test), t_test, target_names=['setosa', 'versicolor', 'virginica'])

    from sklearn.cross_validation import cross_val_score
    # cross validation with 6 iterations 
    scores = cross_val_score(classifier, data, t, cv=6)
    print scores

    from numpy import mean
    print mean(scores)


def test_clustering():
    from sklearn.cluster import KMeans 
    kmeans = KMeans(k=3, init='random') # initialization
    kmeans.fit(data) # actual execution

    c = kmeans.predict(data)

    from sklearn.metrics import completeness_score, homogeneity_score
    print completeness_score(t,c)

    print homogeneity_score(t,c)

    figure()
    subplot(211) # top figure with the real classes
    plot(data[t==1,0],data[t==1,2],'bo')
    plot(data[t==2,0],data[t==2,2],'ro')
    plot(data[t==3,0],data[t==3,2],'go')
    subplot(212) # bottom figure with classes assigned automatically
    plot(data[c==1,0],data[tt==1,2],'bo',alpha=.7)
    plot(data[c==2,0],data[tt==2,2],'go',alpha=.7)
    plot(data[c==0,0],data[tt==0,2],'mo',alpha=.7)
    show()


def test_regression():
    from numpy.random import rand
    x = rand(40,1) # explanatory variable
    y = x*x*x+rand(40,1)/5 # depentend variable

    from sklearn.linear_model import LinearRegression
    linreg = LinearRegression()
    linreg.fit(x,y)

    from numpy import linspace, matrix
    xx = linspace(0,1,40)
    plot(x,y,'o',xx,linreg.predict(matrix(xx).T),'--r')
    show()
        
    from sklearn.metrics import mean_squared_error
    print mean_squared_error(linreg.predict(x),y)

    from numpy import corrcoef
    corr = corrcoef(data.T) # .T gives the transpose
    print corr


    from pylab import pcolor, colorbar, xticks, yticks
    from numpy import arrange
    pcolor(corr)
    colorbar() # add
    # arranging the names of the variables on the axis
    xticks(arange(0.5,4.5),['sepal length',  'sepal width', 'petal length', 'petal width'],rotation=-20)
    yticks(arange(0.5,4.5),['sepal length',  'sepal width', 'petal length', 'petal width'],rotation=-20)
    show()


def test_dimensionalityReduction():
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)

    pcad = pca.fit_transform(data)
    plot(pcad[target=='setosa',0],pcad[target=='setosa',1],'bo')
    plot(pcad[target=='versicolor',0],pcad[target=='versicolor',1],'ro')
    plot(pcad[target=='virginica',0],pcad[target=='virginica',1],'go')
    show()

    print pca.explained_variance_ratio_
    print 1-sum(pca.explained_variance_ratio_)

    data_inv = pca.inverse_transform(pcad)
    print abs(sum(sum(data - data_inv)))

    for i in range(1,5):
        pca = PCA(n_components=i)
        pca.fit(data)
        print sum(pca.explained_variance_ratio_) * 100,'%'



def networks_mining():
    import networkx as nx
    G = nx.read_gml('lesmiserables.gml',relabel=True)
    nx.draw(G,node_size=0,edge_color='b',alpha=.2,font_size=7)

    deg = nx.degree(G)
    from numpy import percentile, mean, median
    print min(deg.values())
    print percentile(deg.values(),25) # computes the 1st quartile
    print median(deg.values())
    print percentile(deg.values(),75) # computes the 3rd quartile
    print max(deg.values())

    Gt = G.copy()
    dn = nx.degree(Gt)
    for n in Gt.nodes():
        if dn[n] <= 10:
            Gt.remove_node(n)
    nx.draw(Gt,node_size=0,edge_color='b',alpha=.2,font_size=12)

    from networkx import find_cliques
    cliques = list(find_cliques(G))

    print max(cliques, key=lambda l: len(l))
