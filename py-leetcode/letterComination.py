

def letterCombination(digits):
    if not digits:
        return []

    key={'1':'1','2':'abc','3':'def','4':'ghi','5':'jkl',
         '6':'mno','7':'pqrs','8':'tuv','9':'wxyz',
         '*':'*','0':'0','#':'#'}

    res=[[]]
    result = list(key[digits[0]])
    for i in digits[1:]:
        temp =[]
        for x in result:
            for k in key[i]:
                temp.append(x+k)
        result=temp

    return result
