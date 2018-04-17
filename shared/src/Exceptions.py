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
class MarvinNotInitialized(Exception):
    """
    Exception raised when Marvin is not initialized and needs to be

    Note:
        THESE MUST BE MODIFIED TO INCLUDE AUTOMATIC LOGGING

    raises a SystemExit
    """
    def __init__(self,*args,**kwargs):
        super(MarvinNotInitialized,self).__init__(*args,**kwargs)
        error_message = "Marvin must be initialized before most processes can occur"
        print(marvin.color_text(error_message,'r',None,'bold'))
        raise SystemExit

class PayloadConnectionError(Exception):
    """
    Exception meant to be raised when their is a problem reading a frame from
    a camera

    Note:
        THESE MUST BE MODIFIED TO INCLUDE AUTOMATIC LOGGING

    does NOT raise a SystemExit
    """
    def __init__(self,*args,**kwargs):
        super(MarvinCameraException,self).__init__(*args,**kwargs)
        # cam_string = str(cam_id) if not marvin.typeCheck(cam_id,None) else "UNKNOWN"
        # error_message = """problem reading frame off of camera '{0}'. is camera connected""".format(cam_string)
        # print(marvin.textColor(error_message,'r',None,'bold'))

class PayloadUserFuncNotFound(Exception):
    """Exception to be raised when in Payload.run_user_func when the
    user function doesn't exist

    Note:
        THESE MUST BE MODIFIED TO INCLUDE AUTOMATIC LOGGING

    does NOT raise a SystemExit
    """
    def __init__(self,*args,**kwargs):
        super(PayloadUserFuncNotFound,self).__init__(*args,**kwargs)



# class FrameTypeError(Exception):
#     """
#     Exception meant to be raised when an incorrect type is passed into
#
#     does NOT raise a SystemExit
#     """
#     def __init__(self,cam_id=None,*args,**kwargs):
#         super(MarvinCameraException,self).__init__(*args,**kwargs)
#         cam_string = str(cam_id) if not marvin.typeCheck(cam_id,None) else "UNKNOWN"
#         error_message = """problem reading frame off of camera '{0}'. is camera connected""".format(cam_string)
#         print(marvin.textColor(error_message,'r',None,'bold'))
