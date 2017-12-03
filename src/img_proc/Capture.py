import cv2
import marvin
import numpy as np

class CameraCapture(object):
    """
    Wrapper class for openCV VideoCapture. This simplifies it's use by replacing
    the cumbersome setting and getting functions by using properties

    input::
        cam_id (int,str): camera id, this can be a video file, a camera path of
                    the type ('/dev/video#'), or an integer id (the last number in the camera path)
        fourcc (str,tuple,list): fourcc code for the video codec to be forced off the camera,
                        reccomend sticking with MJPG as it is supported by most
                        cammeras and generally results in a high framerate even
                        on cheap camera hardware

    attributes::
        cap (cv2.VideoCapture): camera capture object
        _fourcc (str,tuple,list): current fourcc code
        _fourcc_val: current fourcc_val ( VideoCapture_fourcc(fourcc) )

    functions::
        read(): reads image frame
        __setProp(): sets camera property
        __getProp(): gets camera property
        __debugFrame(): generates a static debuging frame

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
    def __init__(self,cam_id=0,fourcc="MJPG"):
        if marvin.typeCheck(cam_id,str):
            if "/dev/video" in cam_id:
                cam_id = int( cam_id.replace("/dev/video","") )
        self.cap = cv2.VideoCapture(cam_id)
        self._fourcc = fourcc
        self._fourcc_val = cv2.VideoWriter_fourcc(*self._fourcc)
        self.__setProp(cv2.CAP_PROP_FOURCC,self._fourcc_val)


    def read(self):
        """
        reads an image from the capture stream, returns a static debug frame if
        it fails to read the frame

        input::
            None
        return::
            image frame from the Capture Stream or static debug frame if reading fails
        """
        status = False
        if self.cap.isOpened():
            status,frame = self.cap.read()
        if not status or not self.cap.isOpened():
            frame = self.__debugFrame()

        return frame

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
            None
        """
        return self.cap.get()

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

    #width
    @property
    def width(self):
        return self.__getProp(cv2.CAP_PROP_FRAME_WIDTH)
    @width.setter
    def width(self,value):
        self.__setProp(cv2.CAP_PROP_FRAME_WIDTH,value)

    #height
    @property
    def height(self):
        return self.__getProp(cv2.CAP_PROP_FRAME_HEIGHT)
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
    viewer = marvin.Cv2ImageViewer("video test")
    timer = marvin.Timer()

    cap.exposure = 1000

    timer.countdown = 10
    while timer.countdown:
        frame = cap.read()
        viewer.view(frame)
        print(timer.countdown)
