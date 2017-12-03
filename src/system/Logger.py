import os
import logging
import marvin

class BaseLogger(object):
    """base class inherited by other loggers"""
    def __init__(self,
                log_level=logging.INFO,
                filename="baselog.log",
                log_format="%(levelname)s:%(message)s"):
        basename = filename
        self.log_level = log_level
        self.filename = filename
        self.log_format = log_format
        self.logger = logging.getLogger(basename)
        self.logger.addHandler(logging.NullHandler())
        logging.basicConfig(filename=self.filename,
                                level=self.log_level,
                                format=self.log_format)
        self.output_attribs = {logging.DEBUG  :{"color":"b","background":None,"attrs":None},
                              logging.INFO    :{"color":"c","background":None,"attrs":"bold"},
                              logging.WARNING :{"color":"y","background":None,"attrs":"bold"},
                              logging.ERROR   :{"color":"r","background":None,"attrs":"bold"},
                              logging.CRITICAL:{"color":"r","background":None,"attrs":None},
                             }
        self.level_text = {logging.DEBUG  : "   DEBUG   |  ",
                          logging.INFO    : "   INFO    |  ",
                          logging.WARNING : "  WARNING  |  ",
                          logging.ERROR   : "   ERROR   |  ",
                          logging.CRITICAL: "  CRITICAL |  ",
                         }

    def _colorOutput(self,message="default output",log_level=logging.INFO,prefix=""):
        """creates a colored logging output for printing to terminal"""
        kwargs = self.output_attribs[log_level]
        level_text = self.level_text[log_level]
        output = marvin.textColor(prefix + level_text + message,**kwargs)
        return output

    def _debug(self,message):
        """
        logs using logging.DEBUG
        input::
            message (str): message to be logged
        return::
            shouldPrint (bool): indicator indicating whether or not the log_level
            is less than the message priorty. This is used by Loggers inheritating
            from this function to determine if they should print
        """
        self.logger.debug(message)
        shouldPrint = False
        if self.log_level <= logging.DEBUG and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _info(self,message):
        """
        logs using logging.INFO
        input::
            message (str): message to be logged
        return::
            shouldPrint (bool): indicator indicating whether or not the log_level
            is less than the message priorty. This is used by Loggers inheritating
            from this function to determine if they should print
        """
        self.logger.info(message)
        shouldPrint = False
        if self.log_level <= logging.INFO and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _warning(self,message):
        """
        logs using logging.WARNING
        input::
            message (str): message to be logged
        return::
            shouldPrint (bool): indicator indicating whether or not the log_level
            is less than the message priorty. This is used by Loggers inheritating
            from this function to determine if they should print
        """
        self.logger.warning(message)
        shouldPrint = False
        if self.log_level <= logging.WARNING and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _error(self,message):
        """
        logs using logging.ERROR
        input::
            message (str): message to be logged
        return::
            shouldPrint (bool): indicator indicating whether or not the log_level
            is less than the message priorty. This is used by Loggers inheritating
            from this function to determine if they should print
        """
        self.logger.error(message)
        shouldPrint = False
        if self.log_level <= logging.ERROR and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint

    def _critical(self,message):
        """
        logs using logging.CRITICAL
        input::
            message (str): message to be logged
        return::
            shouldPrint (bool): indicator indicating whether or not the log_level
            is less than the message priorty. This is used by Loggers inheritating
            from this function to determine if they should print
        """
        self.logger.critical(message)
        shouldPrint = False
        if self.log_level <= logging.CRITICAL and isinstance(self.filename,str):
            shouldPrint = True
        return shouldPrint



class StatusLogger(BaseLogger):
    def __init__(self,*args):
        BaseLogger.__init__(self,*args)

    def debug(self,message):
        """
        logging with logging.DEBUG and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        shouldPrint = self._debug(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.DEBUG,"STATUS | ") )

    def info(self,message):
        shouldPrint = self._info(message)
        """
        logging with logging.INFO and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        if shouldPrint:
            print( self._colorOutput(message,logging.INFO,"STATUS | ") )

    def warning(self,message):
        """
        logging with logging.WARNING and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        shouldPrint = self._warning(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.WARNING,"STATUS | ") )

    def error(self,message):
        """
        logging with logging.ERROR and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        shouldPrint = self._error(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.ERROR,"STATUS | ") )

    def critical(self,message):
        """
        logging with logging.CRITICAL and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        shouldPrint = self._critical(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.CRITICAL,"STATUS | ") )

    def explode(self,message):
        """
        logging with logging.CRITICAL and prints to terminal if it's above the log_level

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        shouldPrint = self._critical(message)
        self._critical("CRITICAL ERROR OCCURED! closing MARVIN..")
        if shouldPrint:
            print( self._colorOutput(message,logging.CRITICAL,"STATUS | ") )
            print(self._colorOutput("closing SAM",logging.CRITICAL) )
        marvin.explode()


class EventLogger(BaseLogger):
    def __init__(self,*args):
        BaseLogger.__init__(self,*args)
        self.timer = marvin.Timer()

    def resetTimer(self):
        """
        resets the timer in the logger, generally used right before an event you
        want to precisely time
        """
        self.timer.reset()

    def debug(self,message):
        """
        logging with logging.DEBUG and prints to terminal if it's above the log_level along with a lap time

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._debug(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.DEBUG,"EVENT  | ") )

    def info(self,message):
        """
        logging with logging.INFO and prints to terminal if it's above the log_level along with a lap time

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._info(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.INFO,"EVENT  | ") )

    def warning(self,message):
        """
        logging with logging.WARNING and prints to terminal if it's above the log_level along with a lap time

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._warning(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.WARNING,"EVENT  | ") )

    def error(self,message):
        """
        logging with logging.ERROR and prints to terminal if it's above the log_level along with a lap time

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._error(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.ERROR,"EVENT  | ") )

    def critical(self,message):
        """
        logging with logging.CRITICAL and prints to terminal if it's above the log_level along with a lap time

        input::
            message (str): message to log and print (if log_level is less than message priorty)
        return::
            None
        """
        message = message + "  |  {0}ms".format( round(self.timer.lap/1000.0,2) )
        shouldPrint = self._critical(message)
        if shouldPrint:
            print( self._colorOutput(message,logging.CRITICAL,"EVENT  | ") )



if __name__ == "__main__":
    base = BaseLogger(20,"testlogger.log")
    print("setting StatusLogger to {0}".format( logging.DEBUG ))
    status = StatusLogger(logging.DEBUG,"testlogger.log")
    print("setting EventLogger to {0}".format( logging.WARNING ))
    event = EventLogger(logging.WARNING,"testlogger.log")

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
