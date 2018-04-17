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
import os
import traceback
import sys

def debug(exception,raise_system_exit=True,message=""):
    """
    simplifies the debugging traceback dialogue by printing a simplified
    version of the traceback to the terminal.
    After printing, this function raises a SystemExit
    input::
        exception (Exception): exception
        raise_system_exit (bool) = True:
            boolean indicating whether to raise a SystemExit
        message (str) = "":
            additional message to print, if desired
    return::
        None
    """
    if message != "": "\r\n\r\nNote: "+message
    # f = outerFile()
    # lineno = outerLineno()
    exc_type,_,tb = sys.exc_info()
    f = os.path.split(tb.tb_frame.f_code.co_filename)[1]
    lineno = tb.tb_lineno
    traceback.print_tb(tb)
    print(marvin.color_text(
"""
===============================================================
                    |  initital traceback  |
file: {filename}
lineno: {lineno}
type: {exc_type}

exception: {exception} {message}
===============================================================
""".format(filename=f,
            lineno=lineno,
            exc_type=exc_type,
            exception=exception,
            message=message),
color='red'))
    if raise_system_exit:
        raise SystemExit


def debug_wrapper(func):
    """decorator wrapper for marvin.debug()"""
    def inner(*args,**kwargs):
        try:
            ret = func(*args,**kwargs)
            return ret
        except Exception as e:
            marvin.debug(e,
                    message="initial func: {name}".format(name=func.__name__))
    return inner
