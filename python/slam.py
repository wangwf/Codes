def slam():

    #dim
    dim = 2*(N + num_landmarks)

    #constraints
    Omega = matrix()
    Omega.zero(dim, dim)
    Omega.value[0][0] = 1.0
    Omega.value[1][1] = 1.0

    Xi = matrix()
    Xi.zero(dim, 1)
    Xi.value[0][0] = world_size/2.0
    Xi.value[1][0] = world_size/2.0

    #process the data

    for k in range(len(data)):
        # index of the robot pose in matrix/vector
        n = k*2

        measurement = data[k][0]
        motion      = data[k][1]

        #integrate the measurement
        for i in range(len(measurement)):
            #m the index of landmark coordinate
            m = 2* (N + measurement[i][0])

            #updata based on the measurement
            for b in range(2):
                Omega.value[n+b][n+b] +=  1.0/measurement_noise
                Omega.value[m+b][m+b] +=  1.0/measurement_noise
                Omega.value[n+b][m+b] += -1.0/measurement_noise
                Omega.value[m+b][n+b] += -1.0/measurement_noise
                Xi.value[n+b][0]      += -measurement[i][1+b]/measurement_noise
                Xi.value[m+b][0]      +=  measurement[i][1+b]/measurement_noise

        #update the information matriax/vector based on the robot motion
        for b in range(4):
            Omega.value[n+b][n+b] += 1.0/motion_noise
        for b in range(2):
            Omega.value[n+b  ][n+b+2] += -1.0/motion_noise
            Omega.value[n+b+2][n+b  ] += -1.0/motion_noise
            Xi.value[n+b  ][0]        += -motion[b]/motion_noise
            Xi.value[n+b+2][0]        +=  motion[b]/motion_noise

        #compute best estimate
    mu = Omega.inverse()*Xi
    return mu


def online_slam():

    #dim
    dim = 2*(1 + num_landmarks)

    #constraints
    Omega = matrix()
    Omega.zero(dim, dim)
    Omega.value[0][0] = 1.0
    Omega.value[1][1] = 1.0

    Xi = matrix()
    Xi.zero(dim, 1)
    Xi.value[0][0] = world_size/2.0
    Xi.value[1][0] = world_size/2.0

    #process the data

    for k in range(len(data)):

        measurement = data[k][0]
        motion      = data[k][1]

        #integrate the measurement
        for i in range(len(measurement)):
            #m the index of landmark coordinate
            m = 2* (1 + measurement[i][0])

            #updata based on the measurement
            for b in range(2):
                Omega.value[b][b]     +=  1.0/measurement_noise
                Omega.value[m+b][m+b] +=  1.0/measurement_noise
                Omega.value[b][m+b]   += -1.0/measurement_noise
                Omega.value[m+b][b]   += -1.0/measurement_noise
                Xi.value[b][0]        += -measurement[i][1+b]/measurement_noise
                Xi.value[m+b][0]      +=  measurement[i][1+b]/measurement_noise

        #xpand the 
        list = [0, 1] + range(4, dim+2)
        Omega = Omega.expand(dim +2, dim+2, list, list)
        Xi    = Xi.expand(dim+2, 1, list, [0])

        #update the information matriax/vector based on the robot motion
        for b in range(4):
            Omega.value[b][b] += 1.0/motion_noise
        for b in range(2):
            Omega.value[b  ][b+2] += -1.0/motion_noise
            Omega.value[b+2][b  ] += -1.0/motion_noise
            Xi.value[b  ][0]        += -motion[b]/motion_noise
            Xi.value[b+2][0]        +=  motion[b]/motion_noise

        newlist = range(2, len(Omega.value))
        a = Omega.take([0, 1], newlist)
        b = Omega.take([0, 1])
        c = Xi.take([0,1],[0])
        Omega = Omega.take(newlist) - a.transpose() * b.inverse()*a
        Xi    = Xi.take(newlist, [0]) - a.transpose()* b.inverse()*c

        #compute best estimate
    mu = Omega.inverse()*Xi
    return mu
