class MarvinNotInitialized(Exception):
    """
    Exception raised when Marvin is not initialized and needs to be

    raises a SystemExit
    """
    def __init__(self,*args,**kwargs):
        super(MarvinNotInitialized,self).__init__(*args,**kwargs)
        error_message = """Marvin must be initialized before most processes can occur"""
        print(marvin.textColor(error_message,'r',None,'bold'))
        raise SystemExit

class MarvinSerialException(Exception):
    """
    Exception meant to be raised when there is a problem with with talking to a
    serial device

    does NOT raise a SystemExit
    """
    def __init__(self,*args,**kwargs):
        super(MarvinSerialException,self).__init__(*args,**kwargs)
        error_message = """problem writing to the serial bus -- is device still connected"""
        print(marvin.textColor(error_message,'r',None,'bold'))

if __name__ == "__main__":
    print("raising test Exception")
    raise marvin.MarvinNotInitialized

class MarvinCameraException(Exception):
    """
    Exception meant to be raised when their is a problem reading a frame from
    a camera

    does NOT raise a SystemExit
    """
    def __init__(self,cam_id=None,*args,**kwargs):
        super(MarvinCameraException,self).__init__(*args,**kwargs)
        cam_string = str(cam_id) if not marvin.typeCheck(cam_id,None) else "UNKNOWN"
        error_message = """problem reading frame off of camera '{0}'. is camera connected""".format(cam_string)
        print(marvin.textColor(error_message,'r',None,'bold'))
#
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
