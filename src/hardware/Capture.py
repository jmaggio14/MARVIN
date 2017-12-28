import cv2
import marvin
import numpy as np
import time

class CameraCapture(object):
    """
    Wrapper class for openCV VideoCapture. This simplifies it's use by replacing
    the cumbersome setting and getting functions by using properties

    input::
        cam_id (int,str): camera id, this can be a video file, a camera path of
                    the type ('/dev/video#'), or an integer id (the last number in the camera path)
        fourcc (str,tuple,list): fourcc code for the video codec to be forced off the camera,
                        reccomend sticking with None for MJPG (the default) as it is supported by most
                        cameras and generally results in a high framerate on cheap camera hardware

    attributes::
        cam_id (str,int): id of the camera being used, passed in as an input
        cap (cv2.VideoCapture): camera capture object
        _fourcc (str,tuple,list): current fourcc code
        _fourcc_val: current fourcc_val ( VideoCapture_fourcc(fourcc) )
        frame_number (int): the number of the last frame
        current_frame_id (str): the id of the last frame, structured "cam_id:frame_number"

    functions::
        read(): reads image frame and returns a marvin.MarvinImage object
        getAllMetadata(): retrieves all metadata at the current state
        [ REMOVED 12/28/17 ] readFrameAndMetadata(): retrieves both the frame and metadata
        __setProp(flag,value): sets camera property
        __getProp(flag): gets camera property
        __debugFrame(): generates a static debuging frame
        __createFrameId(cam_id,frame_number): generates a frame_id

    properties::
        width::
            getter: retrieves width using VideoCapture.get
            setter: sets width using VideoCapture.set
        height::
            getter: retrieves height using VideoCapture.get
            setter: sets height using VideoCapture.set
        fps::
            getter: retrieves fps using VideoCapture.get
            setter: sets fps using VideoCapture.set
        brightness::
            getter: retrieves brightness using VideoCapture.get
            setter: sets brightness using VideoCapture.set
        contast::
            getter: retrieves contast using VideoCapture.get
            setter: sets contast using VideoCapture.set
        hue::
            getter: retrieves hue using VideoCapture.get
            setter: sets hue using VideoCapture.set
        gain::
            getter: retrieves gain using VideoCapture.get
            setter: sets gain using VideoCapture.set
        exposure::
            getter: retrieves exposure using VideoCapture.get
            setter: sets exposure using VideoCapture.set
        writer_dims::
            getter: retrieves image width and height in form (width,height)
            setter: sets writer_dims using VideoCapture.set
        fourcc::
            getter: retrieves the current fourcc code
            setter: sets _fourcc_val using an input fourcc code
        fourcc_val::
            getter: retrieves the current fourcc_val using VideoCapture.get
    """
    def __init__(self,cam_id=0,fourcc=None):
        if fourcc == None:
            fourcc = "MJPG"
        if isinstance(cam_id,str):
            if "/dev/video" in cam_id:
                cam_id = int( cam_id.replace("/dev/video","") )
        self.cam_id = cam_id
        self.cap = cv2.VideoCapture(self.cam_id)
        self._fourcc = fourcc
        self._fourcc_val = cv2.VideoWriter_fourcc(*self._fourcc)
        # setting the codec
        self.__setProp(cv2.CAP_PROP_FOURCC,self._fourcc_val)


        self.frame_number = 0
        self.current_frame_id = self.__createFrameId(self.cam_id,self.frame_number)


    def read(self):
        """
        reads an image from the capture stream, returns a static debug frame if
        it fails to read the frame

        input::
            None
        return::
            frame (marvin.MarvinImage) image frame from the Capture Stream or debugging frame
                    if there is a problem with the capture
        """
        status = False
        if self.cap.isOpened():
            status,raw_frame = self.cap.read()
        if not status or not self.cap.isOpened():
            raw_frame = self.__debugFrame()

        #updating the frame number and the current_frame_id
        self.frame_number += 1
        metadata = self.getAllMetadata()
        frame = marvin.MarvinImage(raw_frame,**metadata)
        return frame

    def getAllMetadata(self):
        """
        UNTESTED!

        grabs all metadata from the frame using the metadata properties and outputs
        it in an easy to use dictionary. also adds key "unix_time", which is the time.time()
        at the time the metadata is collected
        WARNING - what metadata is available is dependent on what camera is attached!

        input::
            None
        return::
            metadata (dict): dictionary containing all metadata values
        """
        self.current_frame_id = self.__createFrameId(self.cam_id,self.frame_number)

        metadata = {
        "width":self.width,
        "height":self.height,
        "fps":self.fps,
        "contrast":self.contrast,
        "brightness":self.brightness,
        "hue":self.hue,
        "gain":self.gain,
        "exposure":self.exposure,
        "writer_dims":self.writer_dims,
        "fourcc":self.fourcc,
        "fourcc_val":self.fourcc_val,
        "capture_time":time.time(),
        "frame_id":self.current_frame_id
        }
        return metadata

    # def readFrameAndMetadata(self):
    #     """
    #     UNTESTED!
    #     returns both the image frame and all associated metadata
    #
    #     input::
    #         None
    #     return::
    #         frame (np.ndarray): frame from the camera, see CameraCapture.read()
    #         metadata (dict): metadata associated with the current frame, see CameraCapture.metadata()
    #     """
    #     frame = self.frame()
    #     metadata = self.metadata()
    #     return frame, metadata

    def __setProp(self,flag,value):
        """
        sets a camera property
        wrapper for VideoCapture.set function

        input::
            flag (opencv constant): flag indicating which property to change
            value (variable): value to set property indicated by the flag

        return::
            None
        """
        return self.cap.set(flag,value)

    def __getProp(self,flag):
        """
        gets a camera property
        wrapper for VideoCapture.get function

        input::
            flag (opencv constant): flag indicating which property to get

        return::
            the camera property requested
        """
        return self.cap.get(flag)

    def __debugFrame(self):
        """
        builds a static debug frame containing text or a shape.

        input::
            None

        return::
            frame (np.ndarray): debug frame
        """
        h,w = self.height,self.width
        if isinstance(h,type(None)) or isinstance(w,type(None)):
            h,w = 256,256

        frame = np.zeros( (h,w), dtype=np.uint8 )
        centroid = marvin.centroid(frame)
        frame = cv2.putText(frame,
                            "error opening or reading image",
                            centroid,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            5,
                            (255,255))
        return frame


    def __createFrameId(self,cam_id,frame_number):
        """
        creates a frame_id from the camera id and the frame number by casting
        the inputs to a string
        frame_id is the in the format "cam_id:frame_number"

        input::
            cam_id (int,str): camera id
            frame_number (int): frame_number

        return::
            frame_id (str): cam_id and frame_number cast to a string for later identification
                            in the form of "cam_id:frame_number"
        """
        frame_id = "{0}:{1}".format(str(cam_id),marvin.fileNumber(frame_number,6))
        return frame_id


    #width
    @property
    def width(self):
        return int(self.__getProp(cv2.CAP_PROP_FRAME_WIDTH))
    @width.setter
    def width(self,value):
        self.__setProp(cv2.CAP_PROP_FRAME_WIDTH,value)

    #height
    @property
    def height(self):
        return int(self.__getProp(cv2.CAP_PROP_FRAME_HEIGHT))
    @height.setter
    def height(self,value):
        self.__setProp(cv2.CAP_PROP_FRAME_HEIGHT,value)

    #fps
    @property
    def fps(self):
        return self.__getProp(cv2.CAP_PROP_FPS)
    @fps.setter
    def fps(self,value):
        self.__setProp(cv2.CAP_PROP_FPS,value)

    #brightness
    @property
    def brightness(self):
        return self.__getProp(cv2.CAP_PROP_BRIGHTNESS)
    @brightness.setter
    def brightness(self,value):
        self.__setProp(cv2.CAP_PROP_BRIGHTNESS,value)

    #contrast
    @property
    def contrast(self):
        return self.__getProp(cv2.CAP_PROP_CONTRAST)
    @contrast.setter
    def contrast(self,value):
        self.__setProp(cv2.CAP_PROP_CONTRAST,value)

    #hue
    @property
    def hue(self):
        return self.__getProp(cv2.CAP_PROP_HUE)
    @hue.setter
    def hue(self,value):
        self.__setProp(cv2.CAP_PROP_HUE,value)

    #gain
    @property
    def gain(self):
        return self.__getProp(cv2.CAP_PROP_GAIN)
    @gain.setter
    def gain(self,value):
        self.__setProp(cv2.CAP_PROP_GAIN,value)

    #exposure
    @property
    def exposure(self):
        return self.__getProp(cv2.CAP_PROP_EXPOSURE)
    @exposure.setter
    def exposure(self,value):
        self.__setProp(cv2.CAP_PROP_EXPOSURE,value)

    #writer_dims
    @property
    def writer_dims(self):
        return self.width,self.height

    #fourcc
    @property
    def fourcc(self):
        return self._fourcc
    @fourcc.setter
    def fourcc(self,value):
        self._fourcc = value
        self._fourcc_val = cv2.VideoWriter_fourcc(*self._fourcc)
        self.__setProp(cv2.CAP_PROP_FOURCC,self._fourcc_val)

    @property
    def fourcc_val(self):
        return self.__getProp(cv2.CAP_PROP_FOURCC)




if __name__ == "__main__":
    marvin.init()
    # cap = GstreamerCapture()
    # timer = marvin.Timer()
    # timer.countdown = 10
    # viewer = marvin.Cv2ImageViewer("gstreamer test")
    #
    #
    # while timer.countdown:
    #     frame = cap.read()
    #     viewer.view(frame)
    print("successful capture test (dependent on a camera being on /dev/video0)")
    cap = CameraCapture("/dev/video0",("M","J","P","G"))
    viewer = marvin.ImageViewer("video test")
    timer = marvin.Timer()

    cap.exposure = 1000

    timer.countdown = 20
    cap.hue = .8
    cap.contrast = .2
    cap.exposure = .6
    while timer.countdown:
        cap.fps = cap.fps - .01
        frame = cap.read()
        print(frame.fps)
        viewer.view(frame)
        print(timer.countdown)
