
def evalRPN(tokens):
    st =[]
    n = len(tokens)
    if n==0: return 0
    op="+-*/"
    for i in range(0, n, 1):
        tok = tokens[i]
        #print tok, n
        if tok in op:
            if len(st)<2: return -1
            a= (st.pop())
            b= (st.pop())
            print a,b,tok
            if   tok == "+": st.append( a + b)
            elif tok == "-": st.append( b - a)
            elif tok == "*": st.append( a * b)
            elif tok == "/": st.append( int(b*1.0/a))
        else:
            st.append(int(tok))

    print(st)
    return int(round(st.pop()))


#alist = ["2", "1", "+", "3", "*"]
#blist = ["4", "13", "5", "/", "+"]
#print evalRPN(alist)
#print evalRPN(blist)
#alist = ["4", "3", "-"]
#print evalRPN(alist)

#alist = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
#print evalRPN(alist)

alist = ["4","13","5","/","+"]
print evalRPN(alist)

