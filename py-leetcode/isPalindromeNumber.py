'''

'''

def isPalindrome(x):
    if x<0:
        return False

    dev =1
    while x/dev>=0: dev *=10;

    while x:
        l = x/dev  # left digit
        r = x%10
        if l != r:
            return False
        x = (x%dev)/10
        dev /= 100

    return True



# using string method
def isPalindrome(x):
    if x<0:
        return False

    s = str(x)
    for i in range(len(s)/2):
        if s[i] != s[len(s) -1 -i]:
            return False
    return True
