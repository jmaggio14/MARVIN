import marvin
import cv2




class HemisphereImager(object):
    def __init__(self,cam_id1,cam_id2,cam_id3,cam_id4):
        self.cap1 = marvin.CameraCapture( cam_id1 )
        self.cap2 = marvin.CameraCapture( cam_id2 )
        self.cap3 = marvin.CameraCapture( cam_id3 )
        self.cap4 = marvin.CameraCapture( cam_id4 )

        self.ORB = cv2.ORB_create()

        self.cache = {"frames":None,
                      "panorama":None}

    def read_frames(self):
        """
        reads frames off of each camera specified
        input::
            None
        return::
            list of frames from each camera
        """
        frames = []
        frames.append( self.cap1.read() )
        frames.append( self.cap2.read() )
        frames.append( self.cap3.read() )
        frames.append( self.cap4.read() )
        self.cache["frame"] = frames
        return frames
