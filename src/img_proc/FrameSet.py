import marvin

class FrameSet(dict):
    """
        A constructor class for a python dictionary -- automatically creates
        a dictionary to index into a MultiCam object

        input::
            cam_ids (list,tuple,marvin.CamId):
                the camera id that the user desires to index into
            key_index (list,)
    """
    def __init__(self,cam_ids,key_index=None):
        if isinstance(cam_ids,marvin.CamId):
            cam_ids = [cam_ids]

        elif isinstance(cam_ids,(int,marvin.FrameId)):
            key_index = [key_index]

        if key_index == None:
            key_index = [0] * len(cam_ids)
        dict.__init__(self,zip(cam_ids,key_index))
