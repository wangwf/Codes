

def plusOne(digits):
    n = len(digits)
    
    l = n-1

    while l>=0:
        if digits[l] !=9:
            digits[l] +=1
            return digits

        digits[l] = 0
        l -=1

    if l == 0:
        return [1] + digits
