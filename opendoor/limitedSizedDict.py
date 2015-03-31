"""

"""
class SizedDict(dict):
    ''' Sized dictionary without timeout. '''

    def __init__(self, size=1000):
        dict.__init__(self)
        self._maxsize = size
        self._stack = []

    def __setitem__(self, name, value):
        if len(self._stack) >= self._maxsize:
            self.__delitem__(self._stack[0])
            del self._stack[0]
        self._stack.append(name)
        return dict.__setitem__(self, name, value)

    # Recommended but not required:
    def get(self, name, default=None, do_set=False):
        try:
            return self.__getitem__(name)
        except KeyError:
            if default is not None:
                if do_set:
                    self.__setitem__(name, default)
                return default
            else:
                raise


#d= SizedDict(2)
#for i in range(10):
#    d[i]=i
#print d, 8 in d

