import os
import logging
import marvin

class BaseLogger(object):
    """base class inherited by other loggers"""
    def __init__(self,
                logLevel=logging.INFO,
                filename="baselog.log",
                logFormat="%(levelname)s:%(message)s"):
        basename = os.path.basename(filename)
        self.logLevel = logLevel
        self.filename = filename
        self.logFormat = logFormat
        self.logger = logging.getLogger(basename)
        self.logger.addHandler(logging.NullHandler())
        logging.basicConfig(filename=self.filename,
                                level=self.logLevel,
                                format=self.logFormat)
        self.output_attribs = {logging.DEBUG  :{"color":"b","background":None,"attrs":None},
                              logging.INFO    :{"color":"c","background":None,"attrs":"bold"},
                              logging.WARNING :{"color":"y","background":None,"attrs":"bold"},
                              logging.ERROR   :{"color":"r","background":None,"attrs":"bold"},
                              logging.CRITICAL:{"color":"r","background":None,"attrs":None},
                             }
        self.level_text = {logging.DEBUG    : "DEBUG    |  ",
                          logging.INFO    : "INFO     |  ",
                          logging.WARNING : "WARNING  |  ",
                          logging.ERROR   : "ERROR    |  ",
                          logging.CRITICAL: "CRITICAL |  ",
                         }

    def _colorOutput(self,message="default output",logLevel=logging.INFO,prefix=""):
        kwargs = self.output_attribs[logLevel]
        level_text = self.level_text[logLevel]
        output = marvin.textColor(prefix + level_text + message,**kwargs)
        return output

    def _debug(self,message):
        """logs using logging.DEBUG"""
        self.logger.debug(message)
        shouldPrint = False
        if self.logLevel >= logging.DEBUG and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _info(self,message):
        """logs using logging.INFO"""
        self.logger.info(message)
        if self.logLevel >= logging.INFO and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _warning(self,message):
        """logs using logging.WARNING"""
        self.logger.warning(message)
        if self.logLevel >= logging.WARNING and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _error(self,message):
        """logs using logging.ERROR"""
        self.logger.error(message)
        if self.logLevel >= logging.ERROR and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _critical(self,message):
        """logs using logging.CRITICAL"""
        self.logger.critical(message)
        if self.logLevel >= logging.CRITICAL and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint



class StatusLogger(BaseLogger):
    def __init__(self,*args):
        BaseLogger.__init__(self,*args)

    def debug(self,message):
        """logging with logging.DEBUG and prints to terminal if it's above the logLevel"""
        shouldPrint = self._debug(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.DEBUG,"STATUS | ") )

    def info(self,message):
        shouldPrint = self._info(message)
        """logging with logging.INFO and prints to terminal if it's above the logLevel"""
        if shouldPrint:
            print( self._colorOutput(message,logging.INFO,"STATUS | ") )

    def warning(self,message):
        """logging with logging.WARNING and prints to terminal if it's above the logLevel"""
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.WARNING,"STATUS | ") )

    def error(self,message):
        """logging with logging.ERROR and prints to terminal if it's above the logLevel"""
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.ERROR,"STATUS | ") )

    def critical(self,message):
        """logging with logging.CRITICAL and prints to terminal if it's above the logLevel"""
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.CRITICAL,"STATUS | ") )


class EventLogger(BaseLogger):
    def __init__(self,*args):
        BaseLogger.__init__(self,*args)
        self.timer = marvin.Timer()

    def resetTimer(self):
        self.timer.reset()

    def debug(self,message):
        """logging with logging.DEBUG and prints to terminal if it's above the logLevel along with a lap time"""
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._debug(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.DEBUG,"EVENT  | ") )

    def info(self,message):
        """logging with logging.INFO and prints to terminal if it's above the logLevel along with a lap time"""
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.INFO,"EVENT  | ") )

    def warning(self,message):
        """logging with logging.WARNING and prints to terminal if it's above the logLevel along with a lap time"""
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.WARNING,"EVENT  | ") )

    def error(self,message):
        """logging with logging.ERROR and prints to terminal if it's above the logLevel along with a lap time"""
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.ERROR,"EVENT  | ") )

    def critical(self,message):
        """logging with logging.CRITICAL and prints to terminal if it's above the logLevel along with a lap time"""
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.CRITICAL,"EVENT  | ") )



if __name__ == "__main__":
    base = BaseLogger()
    status = StatusLogger()
    event = EventLogger()

    status.debug("this is a test")
    status.info("this is a test")
    status.warning("this is a test")
    status.error("this is a test")
    status.critical("this is a test")

    event.debug("this is a test")
    event.info("this is a test")
    event.warning("this is a test")
    event.error("this is a test")
    event.critical("this is a test")
