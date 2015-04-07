

def countAndSay(n):
    say = "1"

    for i in range(n-1):
        next = ""
        for item in [list(g) for k, g in itertools.groupby(say)]:
            next += str(len(item)) + str(item[0])
        say = next

    return say
