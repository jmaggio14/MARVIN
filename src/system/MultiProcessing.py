import multiprocessing
import threading


class NewProcess(multiprocessing.Process):
    """
    Spawns a new process which runs the input target function with the given args
    and kwargs

    This spawns a full new process which can operate on a new CPU

    inherits from multiprocessing.Process
    https://docs.python.org/3.6/library/multiprocessing.html

    input::
        target (func): pointer to the function that runs in this new thread
        *args (unpacked list): arguments for the target func
        **kwargs (unpakced dict): keyword arguments for the target func

    """

    def __init__(self,target,*args,**kwargs):
        super(NewProcess,self).__init__(None,target,None,args,kwargs)
        self.start()

class NewThread(threading.Thread):
    """
    Spawns a new thread which runs the input target function with the given args
    and kwargs

    This thread does NOT initiate a separate process on a new CPU

    inherits from threading.Thread
    https://docs.python.org/3.6/library/threading.html

    input::
        target (func): pointer to the function that runs in this new thread
        *args (unpacked list): arguments for the target func
        **kwargs (unpakced dict): keyword arguments for the target func

    """
    def __init__(self,target,*args,**kwargs):
        super(NewThread,self).__init__(None,target,None,args,kwargs)
        self.start()

class ExitMonitor(object):
    """
    thread safe object to communicate an exit signal to another thread
    MULTITHREADED ISN'T TESTED

    input::
        None

    attributes::
        queue (multiprocessing.Queue): internal queue to make object threadsafe

    functions::
        None

    properties::
        exit_status.getter:
            returns the current exit status, if queue is empty then return False
        exit_status.setter:
            sets the current exit status to the bool(input)
    """
    def __init__(self):
        self.queue = multiprocessing.Queue()

    @property
    def exit_status(self):
        if self.queue.empty():
            return False
        else:
            exit_status = self.queue.get()
            return exit_status
    @exit_status.setter
    def exit_status(self,exit_status):
        self.queue.put( bool(exit_status) )



def infiniteLoop(target,*args,**kwargs):
    """
    runs the given target function with args and kwargs in an infinite loop
    input::
        target (func): target function pointer
        *args (unpacked list): unpacked list of arg
        **kwargs (unpacked dict): unpacked dictionary of keyword arguments
    return::
        None
    """
    while True:
        target(*args,**kwargs)


if __name__ == "__main__":
    pass

    # import time
    # def test(queue):
    #     print( queue.get() )
    #     return
    #
    # def test2():
    #     while True:
    #         print("thread 1")
    #
    # def test3():
    #     while True:
    #         print("thread 2")
    # processes = []
    # print("testing generating 5 processes...")
    # # for i in range(5):
    # q = multiprocessing.Queue()
    # q.put(i*5)
    # q.put("test")
    # p = NewProcess(test2)
    # # print(p.is_alive())
    # p = NewProcess(test3)

        # time.sleep(1)
    # time.sleep(10)
