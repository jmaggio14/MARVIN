import time
import marvin

class Timer(object):
    """
    Timer which can be used to time processes

    attributes::
        _start (float): start time in seconds since the epoch
        _last (float): last time the lap timer was called
        _countdown (float): countdown time if set (recalculated with the countdown property)
        _last_countdown (float): last countdown time check
        __interval_countdown (float): current interval_countdown time
        __last_interval_countdown (float): last interval countdown time

    functions::
        reset(): resets the timer start time

    property::
        time: time since the timer started or was last reset
        lap: time since lap was last accessed (or when timer was created for the first access)
        countdown: countdown time, recalculated every time it's called. never below 0
        countdown.setter: sets the value of countdown
        __interval_countdown: private interval countdown timer for the interval timing
        __interval_countdown.setter: sets the value of interval_countdown

    """
    def __init__(self):
        self._start = time.time()
        self._last = self._start

        self._last_countdown = float(0)
        self._countdown = float(0)

        self._last_interval_countdown = float(0)
        self._interval_countdown = float(0)

    def reset(self):
        """ resets the timer start time """
        self.__init__()

    def runOnInterval(self,interval,func,args,kwargs,Exit_Status=None):
        """
        CURRENTLY HAS AN ISSUE WHERE TIMING TAKES ~50%% longer than the interval specifies!

        runs a fiven function on a specified interval. The user can exit this
        loop using a marvin.ExitStatus object

        while this is operating, the countdown clock is not operational. As with most
        things in python, the timing should be not be relied on for

        input::
            interval (float): time in seconds between function calls
            func (func pointer): pointer to the function to be called on every interval
            args (packed list): list of arguments for 'func'
            kwargs (packed dict): dictionary of keyword arguments for 'func'
            Exit_Status (marvin.ExitStatus): marvin.ExitStatus object,
                if None:: then a placeholder object will be created and the loop will run forever
                if int:: function will be run that number of iterations
        return::
            None
        """
        def run():
            # print(1)
            # print(self.__interval_countdown)
            while self.__interval_countdown:
                continue
            else:
                func(*args,**kwargs)
                self.__interval_countdown = interval

        #checking for infinite run time
        if Exit_Status == None:
            while True:
                run()

        #checking for number of iterations
        elif isinstance(Exit_Status,(int,float)):
            Exit_Status = int(Exit_Status)
            for i in range(Exit_Status):
                run()

        #checking if it's an ExitStatus Queue
        elif isinstance(Exit_Status,marvin.ExitMonitor):
            while not Exit_Status.exit_status:
                run()
        else:
            marvin.Status.critical("run on interval has an unknown exit strategy, (use None for infinite)!!")

    @property
    def time(self):
        """returns the time since the timer started or since it was last reset"""
        return time.time() - self._start

    @property
    def lap(self):
        """returns time since last time the lap was called"""
        now = time.time()
        lap = now - self._last
        self._last = now
        return lap

    @property
    def countdown(self):
        """returns the current countdown time"""
        self._countdown = float(self._countdown) - (self.time - self._last_countdown)
        self._last_countdown = self.time
        if self._countdown < 0:
            self._countdown = 0
        return self._countdown
    @countdown.setter
    def countdown(self,value):
        """sets the countdown timer"""
        if isinstance(value,(int,float)):
            self._countdown = float(value)
        else:
            marvin.Status.critical("countdown must be set using a float or an int, current type is {0}".format(type(value)))

    @property
    def __interval_countdown(self):
        """returns the current interval_countdown time"""
        self._interval_countdown = float(self._interval_countdown) - (self.time - self._last_interval_countdown)
        self._last_interval_countdown = self.time
        if self._interval_countdown < 0:
            self._interval_countdown = 0
        return self._interval_countdown
    @__interval_countdown.setter
    def __interval_countdown(self,value):
        """sets the interval_countdown timer"""
        if isinstance(value,(int,float)):
            self._interval_countdown = float(value)

    @property
    def start(self):
        return self._start



if __name__ == "__main__":
    import time
    timer = Timer()
    timer.countdown = 50
    print(timer.countdown)
    time.sleep(3)
    print(timer.countdown)
    print("reseting...")
    timer.reset()


    #
    # time.sleep(2)
    # print(timer.time)
    # print(timer.lap)
    # time.sleep(2)
    # print(timer.lap)
    # timer.countdown(10)
    # timer.sleep(5)
    # print(timer.countdown)
