#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#
import marvin

Event = None
Status = None
loggers = {}
is_initialized = False

def init(log_level=20,log_filename="output/logs/base_log.log",**logger_kwargs):
    """
    initializes marvin

    currently this only initializes the global Status and Event Loggers used
    throughout marvin to track it's state

    input::
        log_level (int) = 20:
            the log_level for python's logging module.
            standard levels:
                    10-debug,
                    20-info,
                    30-warning,
                    40-error,
                    50-critical
        log_filename (str) = "output/logs/base_log.log":
                the file path for the log file
        **kwargs:
            additional keyword arguments to be passed into
            StatusLogger or EventLogger
    return::
        None
    """
    if not marvin.is_initialized:
        log_filename = marvin.prevent_overwrite(log_filename)
        marvin.Status = marvin.StatusLogger(log_level,
                                                log_filename,
                                                **logger_kwargs)
        marvin.Event = marvin.EventLogger(log_level,
                                                log_filename,
                                                **logger_kwargs)
        marvin.Status.info("marvin is initialized!")
    else:
        marvin.Status.warning("marvin is already initialized!")












#END
