"""
 Sized dictionary
"""
class SizedDict(dict):
    def __init__(self, size=2):
        dict.__init__(self)
        self._maxsize = size
        self._stack = []

    def __setitem__(self, name, value):
        if len(self._stack) >= self._maxsize:
            self.__delitem__(self._stack[0])
            del self._stack[0]
        self._stack.append(name)
        return dict.__setitem__(self,name,value)


if __name__=="__main__":
    d= SizedDict(2)
    for i in range(10):
        d[i]=i
        print i, " ",d
    print d, 8 in d

