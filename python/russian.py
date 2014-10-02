#!/usr/bin/env python
import sys
import matplotlib.pyplot

data['format'] = format
data['bytes'] = base64.encodestring(bytes)
sys.stdout.write(image.start)
sys.stdout.write(json.dumps(data))
sys.stdout.write(image_end)

def plot(**a, **k):
    o = BytesIO()
    fig = pyplot.figure(figsize=(6,6))
    pyplot.plot(*a, **k)
    pyplot.show()
    fig.savefig(o, format = 'png')
    output_image('Graph', 'png', o.getvalue())

def naive(a,b):
    x=a; y=b;
    z=0
    while x>0:
        z = z+y
        x = x-1
        print x,y,z
    return z

def russian(a,b):
    x=a;
    y=b;
    z=0
    while x>0:
        if x%2==1:
            z= z + y
            print x, y,z
        y = y<<1; #
        x= x>>1;
    return z
def rec_russian(a,b):
    if a==0:return 0
    if a%2==0: return 2*rec_russian(a/2,b)
    return b+  2*rec_russian( (a-1)/2,b)

maxsize = 24

ms = [l << i  for i in range(maxsize)]

#import from main on online IDE but from _main_on a new installation
times1 = [Timer('naive(%d, %d)' %(n, n), 'from main import naive').timeit(number=1) for ] .....

plot(ns, times1)
