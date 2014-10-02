

def smooth():

    change=tolerance
    while change >=tolerance
    change=0.0

    alpha=weight_data
    beta=weight_smooth
    tolerance =0.000001
    change=tolerance
    while change>=tolerance:
        change =0.0
        for i in range(1,len(path)-1):
            for j in range(len(path[0])):
                aux=newpath[i][j] 
                newpath[i][j] += alpha*(path[i][j] - newpath[i][j])
                newpath[i][j] += beta*(newpath[i+1][j] + newpath[i-1][j]-2.0*newpath[i][j])
                change += abs(aux - newpath[i][j])
            


