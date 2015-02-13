
import webbrowser

def strToFile(htmlText, htmlFile):
    fw= open(htmlFile,"w")
    fw.write(htmlText)
    fw.close()

def browserHtml(filename):
    with open(filename,"r") as f:
        data = f.read()
    start = 0
    end =0
    hF ="tmp"
    n=1
    while start>-1:
        start = data.find("<!DOCTYPE", end)
        end = data.find("</html>", start)
        print start,end
        if end>start:
            tmpFile = hF+str(n)+".html"
            n +=1
            strToFile(data[start: end+7],tmpFile)
            webbrowser.open_new(tmpFile)


if __name__=="main":
    browserHtml("../dataLogs/learnDataSet.log")
