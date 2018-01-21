import numpy as np
import copy
import marvin
import time
import string
import random
import cv2

class Frame(np.ndarray):
    """
    An image class which inherits from numpy arrays multiple new attributes for the image
    one additional attribute is 'id' which is the frame_id of the frame (usually) in the form of "cam_id:frame_number"
    additional attributes are the metadata the of the image/camera at the time of capture. full list below

    The source of this image metadata comes from the cameras using cv2.VideoCapture.get()
    and the accuracy of the metadata is dependent on the camera being used.
    > MAKE SURE YOU TEST AND RESEARCH YOUR CAMERAS THOROUGHLY BEFORE RELING ON THIS METADATA

    ALL operations normally done on numpy arrays can be done on this image.

    input::
        input_array (np.ndarray,marvin.Frame): Input Array to be cast to a Frame,
                    or another Frame to be reinstantiated as a deep copy with new metadata
        width (int): width of the images (np.ndarray.shape[1])
        height (int): height of the images (np.ndarray.shape[0])
        fps (float): frame rate of the camera at capture
        contrast (float): the contrast of the camera at capture
        brightness (float): the brightness of the camera at capture
        hue (float): the hue of the image at capture
        gain (float): the gain of the image at capture
        exposure (int): the exposure time of the image at capture
        writer_dims (tuple): a (height,width) tuple included for ease of when writer to video
        fourcc (str,tuple,list): 4 character code indicating which codec is used to retrieve images from the camera
        fourcc_val (float): the output of cv2.VideoCapture_fourcc( fourcc )
        capture_time (float): the UNIX time in seconds at capture
        frame_id (str): the id of the new Frame, usually of the form "cam_id:frame_number"

    attributes:: (warning see class description for warnings about metadata accuracy)
        all numpy.ndarray attributes: https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.ndarray.html

        width (int): width of the images (np.ndarray.shape[1])
        height (int): height of the images (np.ndarray.shape[0])
        fps (float): frame rate of the camera at capture
        contrast (float): the contrast of the camera at capture
        brightness (float): the brightness of the camera at capture
        hue (float): the hue of the image at capture
        gain (float): the gain of the image at capture
        exposure (int): the exposure time of the image at capture
        writer_dims (tuple): a (height,width) tuple included for ease of when writer to video
        fourcc (str,tuple,list): 4 character code indicating which codec is used to retrieve images from the camera
        fourcc_val (float): the output of cv2.VideoCapture_fourcc( fourcc )
        capture_time (float): the UNIX time in seconds at capture
        id (str): the unique id for this image
    """
    def __new__(cls,input_array,width,height,fps,contrast,brightness,hue,gain,exposure,writer_dims,fourcc,fourcc_val,capture_time,frame_id):
        # if Frame is passed in, copying the orignal and assigning a new_id
        if isinstance(input_array,marvin.Frame):
            obj = copy.deepcopy(input_array) #deep copy
            obj.width = width
            obj.height = height
            obj.fps = fps
            obj.contrast = contrast
            obj.brightness = brightness
            obj.hue = hue
            obj.gain = gain
            obj.exposure = exposure
            obj.writer_dims = writer_dims
            obj.fourcc = fourcc
            obj.fourcc_val = fourcc_val
            obj.capture_time = capture_time
            obj.id = frame_id

        # if numpy array is passed in, view casting a numpy array and augmenting with an 'id' attribute
        elif isinstance(input_array,np.ndarray) and not isinstance(input_array,marvin.Frame):
            obj = np.asarray(input_array).view(cls) #view casting
            obj.width = width
            obj.height = height
            obj.fps = fps
            obj.contrast = contrast
            obj.brightness = brightness
            obj.hue = hue
            obj.gain = gain
            obj.exposure = exposure
            obj.writer_dims = writer_dims
            obj.fourcc = fourcc
            obj.fourcc_val = fourcc_val
            obj.capture_time = capture_time
            obj.id = frame_id

        # if unacceptable type is passed in, raise a TypeError
        else:
            marvin.Status.critical("attempted to initialize Frame with type({0}) -- must be either {1} or {2}".format(type(input_array),type(np.ndarray),type(marvin.Frame) ))
            raise TypeError

        return obj

    def __array_finalize__(self,obj):
        if obj is None:
            return None
        self.width = getattr(obj,"width",None)
        self.height = getattr(obj,"height",None)
        self.fps = getattr(obj,"fps",None)
        self.contrast = getattr(obj,"contrast",None)
        self.brightness = getattr(obj,"brightness",None)
        self.hue = getattr(obj,"hue",None)
        self.gain = getattr(obj,"gain",None)
        self.exposure = getattr(obj,"exposure",None)
        self.writer_dims = getattr(obj,"writer_dims",None)
        self.fourcc = getattr(obj,"fourcc",None)
        self.fourcc_val = getattr(obj,"fourcc_val",None)
        self.capture_time = getattr(obj,"capture_time",None)
        self.id = getattr(obj,"id",None)


    def __array_wrap__(self,out_arr,context=None):
        return np.ndarray.__array_wrap__(self,out_arr,context)




class DebugFrame(Frame):
    def __new__(cls,message,frame_id="-1:-1",shape=(512,512),dtype=np.uint8):
        metadata = {
                "width":int(-1),
                "height":int(-1),
                "fps":-1.0,
                "contrast":-1.0,
                "brightness":-1.0,
                "hue":-1.0,
                "gain":-1.0,
                "exposure":int(-1),
                "writer_dims":(-1,-1),
                "fourcc":"NONE",
                "fourcc_val":-1.0,
                "capture_time":-1.0,
                "frame_id": marvin.FrameId( frame_id )
                }
        message = str(message)
        input_array = np.zeros( shape, dtype=dtype )
        position = shape[1]//10,shape[0]//2
        input_array = cv2.putText(input_array, str(message), position, cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0))
        input_array = cv2.putText(input_array, "DEBUG FRAME", (0,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
        return Frame.__new__(cls,input_array=input_array,**metadata)



class DebugFrameIncrementor(object):
    def __init__(self):
        self.counter = 0

    def next(self):
        self.counter += 1
        return marvin.DebugFrame(self.counter,marvin.FrameId(-1,self.counter))
# def generateRandomImageMetadata(seed=None):
#     """
#     UNTESTED!!
#
#     generates a set of random metadata that is roughly accurate to what one
#     might expect from a camera (eg. width is never 0 ). Values are based off an
#     input seed. The Exception being the value of metadata["capture_time"] which is
#     equal to time.time()
#     fourcc code and fourcc_val are not corrolated --> they are individually random
#
#     input::
#         seed (int,float): the seed for the random number generator, None to use current time
#     return::
#         metadata (dict): the metadata necessary to build a marvin.Frame object
#     """
#     if seed == None:
#         seed = time.time()
#     RNG = marvin.RandomNumberGenerator( seed )
#
#     width = RNG.randint(50,1000)
#     height = RNG.randint(50,1000)
#     fourcc = randon.sample(string.letters)
#     metadata = {
#             "width":width,
#             "height":height,
#             "fps":round(RNG.rand() * 10,2),
#             "contrast":round(RNG.rand(),2),
#             "brightness":round(RNG.rand(),2),
#             "hue":round(RNG.rand(),2),
#             "gain":round(RNG.rand(),2),
#             "exposure":round(RNG.rand(),2),
#             "writer_dims":(width,height),
#             "fourcc":fourcc,
#             "fourcc_val":round(RNG.rand(),2) * 1000,
#             "capture_time":time.time(),
#             "frame_id": "R"+ ":" + str(RNG.randint(1000))
#             }

if __name__ == "__main__":
    test_src = np.random.rand(512,512)
    test_Image = Frame(test_src,10)

    print("test_Image:\n",test_Image)
    print("test_Image.src == test_Image", test_Image.src == test_Image)

    modified_test_image = test_Image * 10
    print("test_Image + 10:\n",modified_test_image)
