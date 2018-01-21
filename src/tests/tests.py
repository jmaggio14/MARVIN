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
