import marvin
import cv2
from PIL import Image
import numpy as np

class Cv2ImageViewer(object):
    """
    Class to simplify displaying images using opencv windows. Also has
    functionality to resize images automatically if desired

    On some systems (or opencv builds), openCV requires a waitkey to be
    called before displaying the image. This functionality is built in the
    the view function with the argument 'force_waitkey'
    """
    def __init__(self,window_name,size=None,interpolation=cv2.INTER_NEAREST):
        self.window_name = str(window_name)
        self.size = size
        self.interpolation = interpolation
        cv2.namedWindow(self.window_name)

    def view(self,frame,force_waitkey=True):
        """
        displays the frame passed into it
        input::
            frame (np.ndarray): image to be displayed
        return::
            force_waitkey (bool,int): if greater than zero, then call a waitkey
                for the duration of the time given.
                this is required on some systems to display the image properly.
        """
        if isinstance(self.size,(tuple,list)):
            frame = cv2.resize(frame,(self.size[1],self.size[0]),interpolation=self.interpolation)
        cv2.imshow(self.window_name,frame)
        if force_waitkey:
            cv2.waitKey( force_waitkey )


def normalizeAndBin(src,max_count=255,cast_type=np.uint8):
    """
    normalizes and bins the bins the input image to a given bit depth and max_count

    input::
        src (np.ndarray): input image
        max_count (int,float): coefficient to multiple normalized array by
        cast_type (numpy.dtype): numpy dtype the final array is casted to

    return::
        img (np.ndarray): normalized and binned image

    """
    src = src.astype(np.float32)
    src = ( src / src.max() ) * max_count
    src = src.astype(cast_type)
    return src


def quickImageView(img,normalize_and_bin=False):
    """
    quickly displays the image using a PIL Image Viewer

    input::
        img (np.ndarray): input image you want to view
        normalize_and_bin (bool): boolean value indicating whether or not to normalize and bin the image

    return::
        None
    """
    if normalize_and_bin:
        img = normalizeAndBin(img,max_count=255,cast_type=np.uint8)
    img = Image.fromarray( np.flip(img,2) )
    img.show("quickView image")
