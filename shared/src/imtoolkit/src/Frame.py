#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#
import numpy as np
import copy
import marvin
import time
import string
import random
import cv2

class Frame(np.ndarray):
    """
    An image class which inherits from numpy arrays multiple new
    attributes for the image one additional attribute is 'id' which is
    the frame_id of the frame (usually) in the form of
    "cam_id:frame_number" additional attributes are the metadata the of
    the image/camera at the time of capture. full list below

    The source of this image metadata comes from the cameras using
    cv2.VideoCapture.get() and the accuracy of the metadata is dependent
    on the camera being used.
    > MAKE SURE YOU TEST AND RESEARCH YOUR CAMERAS THOROUGHLY BEFORE
     RELYING ON THIS METADATA

    ALL operations normally done on numpy arrays can be done on this
    image. However, they may return a numpy array instead of a Frame obj

    input::
        input_array (np.ndarray,marvin.Frame): Input Array to be cast to
            a Frame, or another Frame to be reinstantiated as a deep
            copy with new metadata

        metadata (dict): dictionary of metadata for the Frame


    attributes:: (warning see class description for warnings about
                    metadata accuracy)
        **all numpy.ndarray attributes**
        https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.ndarray.html
        metadata (dict): dictionary containing metadata for this frame
        frame_id (str): the unique id for this image
    """
    def __new__(cls,input_array,frame_id,metadata):
        # if Frame is passed in, copying the orignal and assign the new
        #metadata and id
        if isinstance(input_array,marvin.Frame):
            obj = copy.deepcopy(input_array) #deep copy
            obj.metadata = metadata
            obj.id = frame_id

        elif isinstance(input_array,np.ndarray):
            obj = np.asarray(input_array).view(cls) #view casting
            obj.metadata = metadata
            obj.id = frame_id

        else:
            marvin.Status.critical("attempted to initialize Frame with\
                                    type({0}) -- must be either \
                                    np.ndarray or marvin.imtoolkit.Frame"
                                    .format( type(input_array) ))
            raise TypeError

        return obj

    def __array_finalize__(self,obj):
        if obj is None:
            return None
        self.metadata = getattr(obj,"metadata",None)
        self.id = getattr(obj,"id",None)


    def __array_wrap__(self,out_arr,context=None):
        return np.ndarray.__array_wrap__(self,out_arr,context)
