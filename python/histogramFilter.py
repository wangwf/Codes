#
# histogram filter for localization
# Monte Carlo filter: discret multi-model

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

p = []

sensor_wrong = 1 - sensor_right
p_stay = 1- p_move

def sense(p, colors, measurement):
    aux = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]

    s=0.0
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (measurement == colors[i][j])
            aux[i][j]= p[i][j]*(hit*sensor_right + (1-hit)*sensor_wrong)
            s += aux[i][j]
    for i in range(len(aux)):
        for j in range(len(aux[i])):
            aux[i][j] /=s
    return aux

def move(p, motion):
#    if motion[1]==0: return p
    q=[[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    for i in range(len(p)):
        for j in range(len(p[i])):
            i1=(i-motion[0])%len(p)
            j1=(j-motion[1])%len(p[i])
            q[i][j]=p[i][j]*p_stay + p[i1][j1]*p_move
    return q

if len(measurements) != len(motions):
    raise ValueError, "error in size of measurement/motion vector"

pinit = 1.0/float(len(colors))/float(len(colors[0]))
p= [[pinit for rwo in range(len(colors[0]))] for col in range(len(colors))]

for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, colors, measurements[k])


#Your probability array must be printed
#with the following code.

show(p)




