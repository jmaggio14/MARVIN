import marvin

Event = None
Status = None
loggers = {}
is_initialized = False
def init(log_level=20,log_filename="output/logs/base_log.log",*args,**kwargs):
    """
    initializes marvin

    currently this only initializes the global Status and Event Loggers used
    throughout marvin to track it's progress

    input::
        log_level (int): the log_level for python's logging module
                standard levels are: 10-debug,20-info,30-warning,40-error,50-critical
        log_filename (str): the file path for the log file
        *args: additional arguments to be passed into StatusLogger or EventLogger
        **kwargs: additional keyword arguments to be passed into StatusLogger or EventLogger
    return::
        generic Status and Event Loggers
    """
    if not marvin.is_initialized:
        log_filename = marvin.preventOverwrite(log_filename)
        marvin.Status = marvin.StatusLogger(log_level,log_filename,*args,**kwargs)
        marvin.Event = marvin.EventLogger(log_level,log_filename,*args,**kwargs)
        marvin.Status.info("sam is initialized!")

        #adding the loggers
        # marvin.addLogger("Status")
    else:
        marvin.Status.warning("sam is already initialized!")

    return marvin.Status,marvin.Event
#
def addLogger(logger_name,log_level=20,logger_type=None,*args,**kwargs):
    """
    adds a logger to the logger dictionary stack

    input::
        logger_name (str): name of the logger that you want to create
        log_level (int): log level
        logger_type (marvin const): type of logger you want to create, either
                    marvin.LOGGER_STATUS or marvin.LOGGER_EVENT as of 11/20/17
    """
    if marvin.typeCheck(logger_type,None): logger_type = marvin.LOGGER_STATUS

    if logger_type == marvin.LOGGER_STATUS:
        marvin.loggers[logger_name] = marvin.StatusLogger(log_level,*args,**kwargs)
    elif logger_type == marvin.LOGGER_EVENT:
        marvin.loggers[logger_name] = marvin.EventLogger(log_level,*args,**kwargs)
    return marvin.loggers[logger_name]


def getLogger(logger_name,*args,**kwargs):
    """
    retrieves a logger
    """
    if logger_name in marvin.loggers.keys():
        out_logger = marvin.loggers[logger_name]
    else:
        out_logger = marvin.addLogger(logger_name,*args,**kwargs)
    return out_logger

if __name__ == "__main__":
    log_level = 20
    filename = "init_function_test.log"
    init(log_level,filename)
    marvin.Status.debug("if you see this, this test failed")
    marvin.Status.critical("it worked!")
    marvin.Event.warning("it worked!")
