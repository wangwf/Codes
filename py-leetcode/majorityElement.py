

def majorityElement(num):
    dict={}
    for i in num:
        dict[i]= dict.get(i,0) +1

    for i, v in dict.iteritems():
        if v>len(num)/2:
            return i

def majorityElement(num):
    res= [num[0],1] #

    for x in num[1:]:
        if x== res[0]: res[1] +=1
        else:
            if res[1]>0: res[1] -=1
            else:
                res=[x,1]

    retrun res[0]
