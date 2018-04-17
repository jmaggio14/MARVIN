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
import time
import sys
import marvin

def pause(pause_time=2,should_print=True):
    """
    sleeps for the specified number of seconds
    input::
        pause_time (int,float) = 2:
                number of seconds to pause
        should_print (bool) = True:
                whether or not to print a warning to terminal that
                pausing has occured
    """
    if should_print:
        marvin.Status.warning("pausing for {0} seconds".format(pause_time))
    time.sleep(2)

def explode():
    """
    calls a system exit
    input::
        None
    return::
        None
    """
    try:
        marvin.Status.critical("emergency exit called! EXITING MARVIN!!!")
    except Exception as e:
        print("possibly a problem with the Status Logger?")
        print("emergency exit called! EXITING MARVIN!!!")
        pass
    sys.exit()
