import cv2
import numpy as np

def debugFrame(self,message="debugging frame",shape=(512,512),dtype=np.uint8):
    """
    builds a black frame with text for an input message, this is meant to be used
    for debugging or to generate false frames

    input::
        message (str): the message to be written on the image

    return::
        frame (np.ndarray): debug frame
    """
    message = str(message)
    frame = np.zeros( shape, dtype=dtype )
    centroid = marvin.centroid(frame)

    frame = cv2.putText(frame, message, centroid, cv2.FONT_HERSHEY_SIMPLEX, 5, (255,255))
    return frame
