import os

DATADIR = ""
DATAFILE = "beatle-diskograph.csv"

def parse_file(datafile):
    data=[]
    with open(datafile, "rb") as f:
        for i in range(11):
            line = f.readline()
            print line
            data.append(line.strip().split(","))

        index = data[0]
        d=[]
        for i in data[1:11]:
            d.append(dict(zip(index,i)))

    return d

#OR

def make_object(keys, values):
    return {keys[i]: values[i] for i in range(len(keys)) }

def parse_line(line):
    return line[:-1].split(",")

def parse_file(datafile):
    with open(datafile, "rb") as f:
        keys = parse_line(f.read())
        return [make_object(keys, parse_line(line)) for line in islice(f, 10)]


#
#
def parse_file(datafile):
    name = ""
    data =[]
    with open(datafile, 'rb') as f:
        r=csv.reader(f)
        name=r.next()[1]
        header=r.next()
        data =[row for row in r] 

    return (name, data)
    

