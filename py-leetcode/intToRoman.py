

def intToRomans(num):
    integers = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    numerals = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]

    res = ""
    for i in range(len(integers)):
        num, remainders = num/integers[i], num%integers[i]
        res += num*numerals[i]
        num = remainders

    return res
