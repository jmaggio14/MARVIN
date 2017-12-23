import marvin
import cv2

class FrameGrabber(object):
    """
    object which is used to capture images from multiple cameras and stores them
    in an internal buffer for access by other processes
    input::
        cam_ids (int,str): list of ids for the openCV VideoCapture class, see marvin.CameraCapture
                for more information
        cache_size (int): the number of frames to cache for each camera in the buffer
        fourccs (list): a list of strings to override the default MJPG fourcc code
    """
    def __init__(self,cam_ids,cache_size=30,fourccs=None):
        self.cam_ids = map(str,cam_ids)

        self.cache_size = int(cache_size)

        if fourccs == None:
            fourccs = ["MJPG"] * len(self.cam_ids)
        self.fourccs = fourccs

        self.caps = self.__createCaptureObjects()

    def __createCaptureObjects(self):
        """
        private to marvin.FrameGrabber

        creates the marvin.CameraCapture objects which will be used to talk to
        each individual camera
        input::
            None
        return::
            caps (dict): dict of marvin.CameraCapture objects created for each camera,
                        the key is the string of the corresponding cam_id
        """
        caps = {}
        for cam_id,fourcc in self.cam_ids,self.fourccs:
            try:
                caps[cam_id].append( marvin.CameraCapture(cam_id,fourcc) )
            except marvin.MarvinCameraException:
                marvin.Status.critcal("unable to connect to camera: {0} with fourcc: {1}".format(cam_id,fourcc))

    def __setupBuffers(self):
        """
        private to marvin.FrameGrabber

        creates the buffers
        """





class CaptureBuffer(object):
    def __init__(self,cache_size):
        self.cache_size = cache_size

    def add(self,):













#END
