import marvin
import cv2

class Cv2ImageViewer(object):
    def __init__(self,window_name,size=None,interpolation=cv2.INTER_NEAREST):
        self.window_name = str(window_name)
        self.size = size
        self.interpolation = interpolation
        cv2.namedWindow(self.window_name)

    def view(self,frame):
        if isinstance(self.size,(tuple,list)):
            frame = cv2.resize(frame,(self.size[1],self.size[0]),interpolation=self.interpolation)
        cv2.imshow(self.window_name,frame)
