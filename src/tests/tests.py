import marvin
import os

def test_debug():
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)
    try:
        raise TypeError
    except Exception as e:
        marvin.debug(e,False)

def test_RandomNumberGenerator():
    """
    tests the RandomNumberGenerator class by printing 1000 uniform random numbers
    """

    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)
    try:

        testing_logger.info("printing 10 random numbers between 0 and 1...")
        a = marvin.RandomNumberGenerator(0)
        for i in range(10):
            print( a.uniform(0,1,1) )

    except Exception as e:
        testing_logger.critical("test_RandomNumberGenerator test failed")
        marvin.debug(e,False)
        return False

    finally:
        return True

def test_Timer():
    import time

    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    timer = marvin.Timer()
    timer.countdown = 50
    testing_logger.info("{0}".format( timer.countdown ))
    time.sleep(3)
    testing_logger.info("{0}".format( timer.countdown ))
    testing_logger.info("reseting...")
    timer.reset()

    testing_logger.info("setting up a interval timer, we should be printing for 'hello world' ever second for 10 seconds")
    def printText(text="Hello, World!"):
        print( time.time()," : ",text )
    args = ("Hello!... also args work!!!",)
    kwargs = {}
    timer.runOnInterval(1.0,printText,args,kwargs,5)

def test_quickImageView():
    import cv2
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    data_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    lenna_path = data_path + "lenna.png"

    img = cv2.imread(lenna_path,cv2.IMREAD_UNCHANGED)
    marvin.quickImageView(img)



def test_CaptureBuffer():
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    # generateRandomImage = lambda : np.random.rand(512.512)

    testing_logger.info("creating camera capture object")
    cap = marvin.CameraCapture()

    testing_logger.info("creating the image viewers")
    cap_viewer = marvin.ImageViewer("raw off the cameras")
    buffer_viewer = marvin.ImageViewer("capture buffer test")

    testing_logger.info("creating the capture buffer")
    buf = marvin.CaptureBuffer()

    timer = marvin.Timer()
    timer.countdown = 30
    testing_logger.info("setting countdown timer to 30seconds")

    while timer.countdown:
        frame = cap.read()
        cap_viewer.view(frame)
        #adding the frame to the buffer
        frame_id = buf.add(frame)
        buffer_viewer.view( buf.getByIndex(15) )
        print("countdown: ",timer.countdown)
    buffer_viewer.close()
    cap_viewer.close()


def test_debugFrame():
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    debug_frame = marvin.debugFrame("test debugging frame")
    marvin.quickImageView( debug_frame )




def test_MultiCam():
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    frame_grabber = marvin.MultiCam( ["/dev/video0"],buffer_size=30,fourccs=["MJPG"] )
    cam_id = frame_grabber.cam_ids[0]
    real_time_viewer = marvin.ImageViewer("MultiCam test -- real time viewer")
    index_15_viewer = marvin.ImageViewer("MultiCam test -- index 15 viewer")

    for i in range(500):
        frame_set = frame_grabber.grab()
        testing_logger.info("grabbing frame {0}, total number of frames in one camera buffer {1}".format(i,len(frame_grabber.frame_sets)) )
        real_time_viewer.view( frame_grabber.retrieve( frame_set )[cam_id] )
        index_15_viewer.view( frame_grabber.retrieve(15)[cam_id] )

    index_15_viewer.close()
    real_time_viewer.close()


def test_Rtsp():
    marvin.init()
    testing_logger = marvin.getLogger("TESTING LOGGER",log_level=10,logger_type=marvin.LOGGER_EVENT)

    incrementor = marvin.DebugFrameIncrementor()
    streamer = marvin.RtspServer(host="127.0.0.1",port=5000)
    viewer = marvin.ImageViewer("RTSP SERVER TEST -- these images will be sent to the server")

    for i in range(10000):
        frame = incrementor.next()
        streamer.write(frame)
        viewer.view(frame)

if __name__ == "__main__":
    marvin.init()

    marvin.Status.warning("testing the debug function...")
    test_debug()

    marvin.Status.warning("testing the RandomNumberGenerator object...")
    test_RandomNumberGenerator()

    marvin.Status.warning("testing the Timer object...")
    test_Timer()

    marvin.Status.warning("testing the quickImageView function...")
    test_quickImageView()
