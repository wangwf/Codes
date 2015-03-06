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
#         print result[i][j], result[i1][j],
#        print result[i][j], result[i2][j]
#        print result[i][j], result[i][j1]
#        print result[i][j], result[i][j2]
#        print i*n+j, i1*n+j, i2*n+j, i*n+j1, i*n+j2
