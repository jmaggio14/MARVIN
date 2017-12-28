import numpy as np
import copy

class MarvinImage(np.ndarray):
    """
    An image class which inherits from numpy arrays
    
    """
    def __new__(cls,input_array,frame_id,ORB=None):
        # building a numpy array and augmenting
        obj = np.asarray(input_array).view(cls)
        obj.id = frame_id
        return obj

    def __array_finalize__(self,obj):
        if obj is None: return None
        self.id = getattr(obj,"id",None)

    def __array_wrap__(self,out_arr,context=None):
        return np.ndarray.__array_wrap__(self,out_arr,context)
    # #
    #

if __name__ == "__main__":
    test_src = np.random.rand(512,512)
    test_Image = MarvinImage(test_src,10)

    print("test_Image:\n",test_Image)
    print("test_Image.src == test_Image", test_Image.src == test_Image)

    modified_test_image = test_Image * 10
    print("test_Image + 10:\n",modified_test_image)
