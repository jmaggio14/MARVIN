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

    attributes::
        cam_ids (list): list of input camera ids, turned to strings
        buffer_size (int): input buffer_size, cast to an integer
        fourccs (list): list of strings, copied from input or if None, then
                    equal to ["MJPG"] * len(self.cam_ids)
        caps (list): list of marvin.CameraCapture objects for each camera, direct output
                    from __createCaptureObjects()
        buffers (list): list of marvin.CaptureBuffer objects, where the output from
                    each cameras is saved


    functions::
        __createCaptureObjects(): creates the marvin.CameraCapture objects used to
                    capture images from the camera
        __createBuffers(): creates the marvin.CaptureBuffer objects used to store
                    images off the cameras
    """
    def __init__(self,cam_ids,buffer_size=30,fourccs=None):
        # self.cam_ids = map(str,cam_ids)
        self.cam_ids = []
        for i in cam_ids:
            self.cam_ids.append( str(i) )

        self.buffer_size = int(buffer_size)

        if fourccs == None:
            fourccs = ["MJPG"] * len(self.cam_ids)
        self.fourccs = fourccs

        self.caps = self.__createCaptureObjects()
        self.buffers = self.__createBuffers()

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
                marvin.Status.info("adding CameraCapture object for cam_id: {0}".format(cam_id))

            except marvin.MarvinCameraException:
                marvin.Status.critcal("unable to connect to camera: {0} with fourcc: {1}".format(cam_id,fourcc))

        return caps

    def __createBuffers(self):
        """
        private to marvin.FrameGrabber

        creates the buffers necessary for temporary storage of frames
        input::
            None
        return::
            buffers (dict): dict of marvin.CaptureBuffer objects created for each
                            camera to store the frames in a temporary manner
                            the key is the corresponding frame id
        """
        buffers = {}
        for cam_id in self.caps.keys():
            buffers[cam_id] = marvin.CaptureBuffer(self.buffer_size)
            marvin.Status.info("adding CaptureBuffer object for cam_id: {0}".format(cam_id))
        return buffers



    def grab(self):
        """
        grabs images from all the cameras, puts them in Frame Containers, and
        stores them in the buffers


        """
        for cam_id in self.caps.keys():
            raw_frame,raw_frame_metadata = self.caps[cam_id].readFrameAndMetadata()
            frame_container = marvin.FrameContainer(raw_frame,raw_frame_metadata)
            self.buffers[cam_id].add( frame_container )



#END
