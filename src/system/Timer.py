import time

class Timer(object):
    """
    Timer which can be used to time processes

    attributes::
        _start: start time in seconds since the epoch
        _last: last time the lap timer was called
        _countdown: countdown time if set (recalculated with the countdown property)

    functions::
        reset(): resets the timer start time

    property::
        time: time since the timer started or was last reset
        lap: time since lap was last accessed (or when timer was created for the first access)
        countdown: countdown time, recalculated every time it's called. never below 0
        countdown.setter: sets the value of countdown

    """
    def __init__(self):
        self._start = time.time()
        self._last = self._start
        self._last_countdown = float(0)
        self._countdown = float(0)

    def reset(self):
        """ resets the timer start time """
        self._start = time.time()

    def set_countdown(self,value):
        self.countdown = value

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

    @property
    def start(self):
        return self._start



if __name__ == "__main__":
    import time
    timer = Timer()
    timer.countdown = 5
    print(timer.countdown)
    time.sleep(3)
    print(timer.countdown)


    #
    # time.sleep(2)
    # print(timer.time)
    # print(timer.lap)
    # time.sleep(2)
    # print(timer.lap)
    # timer.countdown(10)
    # timer.sleep(5)
    # print(timer.countdown)
