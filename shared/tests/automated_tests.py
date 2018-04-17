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

## ---------------- TESTS FOR WHOLE FILES --------------------
#constants.py
def test__constants():
    """
    checks to make sure necessary constants are defined in marvin

    input::
        None
    returns::
        ret (bool):
            boolean indicating whether or not the test was passed

    """
    import marvin
    required_constants = [
                            #GPIO constants
                            "GPIO_INPUT","GPIO_OUTPUT","GPIO_HIGH","GPIO_LOW",
                            #LOGGER constants
                            "LOGGER_STATUS","LOGGER_EVENT",
                            #GSTREAMER constants
                            "GSTREAMER_ENCODER_X264","GSTREAMER_ENCODER_OMX264"
                            ]
    ret = True
    for const in required_constants:
        #checking to see if the constant exists
        exists = hasattr(marvin,const)
        if not exists:
            error_msg = "MISSING CONSTANT marvin.{const}".format(const=const))
            ret = False

    return ret

#init.py
def test__init():
    """tests marvin's init function

    input::
        None

    returns::
        ret (bool):
            boolean indicating whether or not the test was passed

    """
    import marvin
    import sys
    import traceback
    #running the init Function
    try:
        marvin.init()
    except Exception as e:
        exc_type,_,tb = sys.exc_info()
        traceback.print_tb()
        print('init() failed with exception {e}'.format(e=e))
        raise SystemExit

    #checking for status logger
    if hasattr(marvin,"Status"):
        if isinstance(marvin.Status,marvin.StatusLogger):
            has_status = True
        else:
            has_status = False
    else:
        has_status = False
    if not has_status:
        print("failed to initialize Status Logger")

    #checking for event logger
    if hasattr(marvin,"Event"):
        if isinstance(marvin.Event,marvin.EventLogger):
            has_event = True
        else:
            has_event = False
    else:
        has_event = False
    if not has_event:
        print("failed to initialize Event Logger")


    ret = has_status and has_event
    return ret


def test__Logger_depreciated():
    pass

def test__retry_on_fail():
    pass


## ---------------- TESTS FOR INDIVIDUAL OBJECTS --------------------
#misc.py
def test__pause():
    pass

#misc.py
def test__explode():
    pass

#output.py
def test__prevent_overwrite():
    pass

#output.py
def test__make_numbered_prefix():
    pass
