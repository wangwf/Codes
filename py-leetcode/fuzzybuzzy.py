
def fuzzybuzzy(n):
    word1 = "fuzzy"
    word2 = "buzzy"
    res=""
    if n%3==0: res += word1
    if n%5==0: res += word2
    if len(res)>0:
        print n, res

for i in range(100):
    fuzzybuzzy(i)
