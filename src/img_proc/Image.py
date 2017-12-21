import numpy as np
# import marvin
import copy

class MarvinImage(np.ndarray):
    def __new__(cls,input_array,frame_id):
        # building a numpy array and augmenting
        obj = np.asarray(input_array).view(cls)
        obj.src = copy.copy(obj)

        obj.id = str(frame_id)
        return obj

    def __array_finalize__(self,obj):
        if obj is None: return
        # print(dir(obj))
        self.src = getattr(obj,"frame_id",None)
        self.id = getattr(obj,"id",None)

    def __array_wrap__(self,out_arr,context=None):
        return super(MarvinImage,self).__array_wrap__(self,out_arr,context)


if __name__ == "__main__":
    test_src = np.random.rand(512,512)
    test_Image = MarvinImage(test_src,10)

    print("test_Image:\n",test_Image)
    print("test_Image.src:\n",test_Image.src)
    print("test_Image.src == test_Image", test_Image.src == test_Image)

    modified_test_image = test_Image * 10
    print("test_Image + 10:\n",modified_test_image)
