
'''
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.
'''
def isValid(s):
    stack=[]
    p1 = "([{"
    p2 = ")]}"
    for i in range(len(s)):
        if s[i] not in p1+p2:
            continue

        if len(stack)==0:
            if s[i] in p1:
                stack.append(s[i])
            elif s[i] in p2:
                return False
        else:
            top = stack.pop()
            if  (s[i] == p2[0] and top == p1[0]) or \
                (s[i] == p2[1] and top == p1[1]) or \
                (s[i] == p2[2] and top == p1[2]):
                continue
            else:
                if s[i] in p1:
                    stack.append(top)
                    stack.append(s[i])

    return len(stack)==0
            

