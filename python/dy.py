# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value1(x,y):
    if x<0 or x>=len(grid) or y<0 or y>=len(grid[0]):
        return 99
    if grid[x][y]==1:
        return 99
    
    if x==goal[0] and y == goal[1] :
        return 0
    else: 
        left =compute_value(x-1,y)+1
        right=compute_value(x+1, y)+1
        up  = compute_value(x, y-1) +1
        down= compute_value(x, y+1)+1
    value= min(left, right, up, down)

    return value #make sure your function returns a grid of values as demonstrated in the previous video.

#compute_value(init[0],init[1])

def compute_value():
    value =[[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    change = True
    while change:
        change=False

        for x in range(len(grid)):
            for y in range(len(grid[0])):

                if goal[0] == x and goal[1] ==y:
                    if value[x][y] >0:
                        value[x][y]=0
                        policy[x][y]= '*'
                        change = True
                elif grid[x][y]==0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >=0 and x2 < len(grid) and y2 >= 0 and y2 <len(grid[0]) and grid[x2][y2]==0:
                         v2 =  value[x2][y2] + cost_step

                         if v2 <value[x][y]:
                             change = True
                             value[x][y] = v2
                             policy[x][y] = delta_name[a]
    for i in range(len(value)):
        print value[i]

    return value

compute_value()
