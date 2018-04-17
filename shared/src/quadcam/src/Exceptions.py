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

class CaptureBufferIndexError(Exception):
    """
    Exception to be raised when a CaptureBuffer is unable to

    Note:
        THESE MUST BE MODIFIED TO INCLUDE AUTOMATIC LOGGING

    does NOT raise a SystemExit
    """
    def __init__(self,*args,**kwargs):
        if "key_index" in kwargs.keys():
            error_message = "Capture Buffer does not contain an image \
                                specified by the given key_index {0}"
                                .format(kwargs["key_index"])
        else:
            error_message = "Capture Buffer does not contain an image \
                            specified by the given key_index"

        super(MarvinNotInitialized,self).__init__(*args,**kwargs)
        print(marvin.color_text(error_message,'r',None,'bold'))

class CameraException(Exception):
    """
    Exception meant to be raised when there is a problem reading a frame
    from a camera

    does NOT raise a SystemExit
    """
    def __init__(self,cam_id=None,*args,**kwargs):
        super(MarvinCameraException,self).__init__(*args,**kwargs)
        error_message = """problem reading frame off of camera '{0}'.\
                                is camera properly connected?""".format(cam_id)
        print(marvin.color_text(error_message,color='red',attrs='bold'))
