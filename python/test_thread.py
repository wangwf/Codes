import Queue
import threading
import urllib2

worker_data =['http://google.com', 'http://yahoo.com','http://bing.com']

# a queue
q=Queue.Queue()
for url in worker_data:
    q.put(url)

#define a worker function
def worker(queue):
    queue_full=True
    while queue_full:
        try:
            url=queue.get(False)
            data = urllib2.urlopen(url).read()
            print len(data),url
        except Queue.Empty:
            queue_full = False

#create number of threads
def test_thread1():
    thread_count=5
    for i in range(thread_count):
        t=threading.Thread(target=worker, args =(q,))
        t.start()

#test_thread1()

class SummingThread(threading.Thread):
    def __init__(self, low, high):
        threading.Thread.__init__(self)
        self.low = low
        self.high= high
        self.total =0

    def run(self):
        for i in range(self.low, self.high):
            self.total += i

def test_thread2():
    thread1 = SummingThread(0,500000)
    thread2 = SummingThread(500000, 1000000)
    thread1.start() # This actually causes the thread to run
    thread2.start()
    thread1.join() # This waits until the thread has completed
    thread2.join()

    result = thread1.total + thread2.total
    print  thread1.total, " + ",thread2.total," = ", result


#test_thread2()


class Monitor(threading.Thread):
    def __init__(self, mon):
        threading.Thread.__init__(self)
        self.mon = mon
        self.status=True

    def run(self):
        while self.status:
            if self.mon[0] == 2:
                print "Mon = 2"
                self.mon[0] =3
    def stop(self):
        self.status=False

def test_asynchronous():
    a=[0]
    mon=Monitor(a)
    mon.start()
    a[0]=2
    print a
    a[0]=2

    mon.stop()
    a[0]=2

test_asynchronous()

