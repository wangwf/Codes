result=[]
with open("placement.txt","r") as f:
    for line in f:
        result.append(line.split())

result

n=len(result)
m=len(result[0])
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

