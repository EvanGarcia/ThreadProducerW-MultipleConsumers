from random import randrange
from time import sleep
from queue import Queue, Empty
from myThread3 import MyThread
import threading

#Get input from user
NITEMS = int(input("Enter number of items: "))
NREADERS = int(input("Enter number of readers: "))
WRITERDELAY = float(input("Enter writer delay: "))

def writeQ(queue, item):
    #Puts item into queue
    print('Writer producing object %d for Q...' % item, end='')
    queue.put(item, True)    
    print("size now", queue.qsize())

def readQ(queue, threadName):
    #Gets item from queue. Delays if writer isn't finished and the queue is empty
    if writerFinished == False and queue.empty():
        sleep(1) 
    try:
        val = queue.get(False)
        print('%s consumed object %d from Q... size now' % (threadName, val), queue.qsize())
        return val
    except Empty:
        print('%s polling empty queue' % threadName)
        return None
        
   

def writer(queue, loops): 
    #Runs writeQ and sets writerFinished to true when all producing is finished 
    global writerFinished
    writerFinished = False
    for i in range(loops):
        writeQ(queue, i)
        sleep(WRITERDELAY)
    writerFinished = True            

def reader(queue, loops):
    #Run readQ and exit if writerfinished is equal to true and the queue is empty   
    for i in range(loops):
        item = readQ(queue, threading.current_thread().name)
        sleep(randrange(2,6))
        if writerFinished == True and queue.empty():
            return
        
         
funcs = [writer]


def main(): 
    nloops = NITEMS
    q = Queue(32)

    threads = []

    # Populate functions with however many readers we need
    for i in range(NREADERS):
        funcs.append(reader)
    
    nfuncs = range(len(funcs))

    # Create our writer thread and all of our reader threads
    for i in nfuncs:       
        t = MyThread(funcs[i], (q, nloops), funcs[i].__name__+"-"+str(i-1))        
        threads.append(t)

    for i in nfuncs:     
        threads[i].start()

    for i in nfuncs:      
        threads[i].join()

    print('all DONE')

if __name__ == '__main__':   
    main()