# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------

    closed =[[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]]=1
    expand= [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    action= [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]

    x=init[0]
    y=init[1]
    g=0
    h = heuristic[x][y]
    f = g + h

    open=[[f,g,h, x, y]]

    found = False #flag that is set when search complete
    resign = False #flag set if we can't find expand
    count =0
    while found is False and resign is False:
        #check if we still have elements on the open list
        if len(open) == 0:
            resign = True
            print 'fail'
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[3]
            y = next[4]
            g = next[1]
#            h = next[1] 
#            f = next[0]

            expand[x][y]=count
            count +=1

            # check if we are don

            if x == goal[0] and y == goal[1]:
                found = True
                print next
                return next
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2>=0 and x2< len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] ==0:
                            g2= g + cost
                            h2= heuristic[x2][y2]
                            f2=g2+h2
                            open.append([f2,g2,h2, x2, y2])
                            closed[x2][y2] =1
                            action[x2][y2] =i

    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    x = goal[0]
    y = goal[1]
    policy[x][y] = '*'
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        x = x2
        y = y2

    for i in range(len(policy)):
        print policy[i]

    return open# path # you should RETURN your result

search()
