import cv2
import marvin

class Cv2VideoWriter(object):
    """
    a wrapper class for the cv2 Video Writer:
    https://docs.opencv.org/3.0-beta/modules/videoio/doc/reading_and_writing_video.html#videowriter-fourcc
    """
    def __init__(self,filename="out_video.avi",fps=30.0,fourcc="XVID"):
        self.filename = marvin.preventOverwrite(filename)
        self._fourcc = fourcc
        self._fourcc_val = cv2.VideoWriter_fourcc(*self._fourcc)
        self._fps = float(fps)
        self.__is_initialized = False

    def __init(self,size):
        """
        opens and initializes the videowriter
        """
        marvin.Status.info("initializing the VideoWriter...")
        self._h,self._w = size
        self.kwargs = {"filename"  :self.filename,
                        "fourcc"   :self._fourcc_val,
                        "fps"      :self._fps,
                        "frameSize":(self._w,self._h)
                        }
        self.writer = cv2.VideoWriter( **self.kwargs )
        self.__is_initialized = True

    def write(self,frame):
        """
        writes a frame to the video file.
        automatically opens a video writer set to the input frame size
            frame: input frame to save to file
        return::
            None
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        if not self.writer.isOpened():
            self.writer.open( **self.kwargs )

        self.writer.write(frame)

    def release(self):
        """
        closes the video writer, ironically creates opens the videowriter
        if it's not already open
        input::
            None
        return::
            None
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        self.writer.release()

    def reopen(self):
        """
        closes and reopens the VideoWriter. ironically creating it if it doesn't
        exist
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        if self.writer.isOpened():
            self.writer.release()
        self.writer.open( **self.kwargs )

if __name__ == "__main__":
    marvin.init()
    print(
    marvin.textColor(
    """
    testing the video writer by taking videos from a camera, relies on a camera
    being attached to /dev/video0!!!
    """,
    "y",None,"bold")
    )
    timer = marvin.Timer()
    cap = marvin.CameraCapture(0)
    writer = marvin.Cv2VideoWriter()
    viewer = marvin.Cv2ImageViewer("video writer test")

    timer.countdown = 15
    while timer.countdown:
        frame = cap.read()
        viewer.view(frame)
        writer.write(frame)
        print(timer.countdown)
    else:
        writer.release()
