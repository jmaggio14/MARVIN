import marvin
import cv2


class Cv2ImageWriter(object):
    def __init__(self,output_dir,base_filename="image.png",size=None,interpolation=cv2.INTER_NEAREST):
        self.output_dir = marvin.preventOverwrite(output_dir)
        self.base_filename = base_filename
        self.size = size
        self.interpolation = interpolation

    def write(self,frame):
        filename = marvin.preventOverwrite(self.base_filename)
        if not isinstance(self.size,type(None)):
            frame = cv2.resize(frame,(self.size[1],self.size[0]),interpolation=self.interpolation)
        cv2.imwrite(filename,frame)
