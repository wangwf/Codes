from pyspark import SparkContent
import csv
import StringIO

def loadRecord(line, fieldnames):
    ''' Parse a csv file '''
    input = StringIO.StringIO(line)
    reader = csv.DictReader(input, filename)

    return reader.next()


def loadRecords(fileNameConents, fieldnames):
    ''' Load all records from a csv file '''
    input = StringIO.StringIO(fileNameContents)
    reader = csv.DictReader(input, filename)

    return reader


def writeRecords(records, fieldnames):
    """Write out CSV lines"""
    output = StringIO.StringIO()
    writer = csv.DictWriter(output, fieldnames) #=["name", "favouriteAnimal"])
    for record in records:
        writer.writerow(record)
    return [output.getvalue()]


def loadJson(inFile):
    ''' Load a json file '''
    import json
    sc = SparkContext(master, "LoadJson")
    input = sc.textFile(inFile)
    data = input.map(lambda x : json.loads(x))
#    data.filter(lambda x: 
    sc.stop()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Error usage: LoadCsv [sparkmaster] [inputfile] [outputfile]"
        sys.exit(-1)
    master = sys.argv[1]
    inputFile = sys.argv[2]
    outputFile = sys.argv[3]
    sc = SparkContext(master, "LoadCsv")
    # Try the record-per-line-input
    input = sc.textFile(inputFile)
    data = input.map(loadRecord)
    pandaLovers = data.filter(lambda x: x['favouriteAnimal'] == "panda")
    pandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile)
    # Try the more whole file input
    fullFileData = sc.wholeTextFiles(inputFile).flatMap(loadRecords)
    fullFilePandaLovers = fullFileData.filter(
        lambda x: x['favouriteAnimal'] == "panda")
    fullFilePandaLovers.mapPartitions(
        writeRecords).saveAsTextFile(outputFile + "fullfile")
    sc.stop()
    print "Done!"



