import marvin


def centroid(frame):
    """
    finds the centroid of the given image frame
    input::
        frame (np.ndarray): input frame to find the centroid of
    return::
        centroid (tuple): centroid of the input image (center pixel coordinates)
    """
    centroid = frame.shape[0]//2,frame.shape[1]//2
    return centroid

def frameSize(frame):
    """
    return the height and width of a given frame
    input::
        frame (np.ndarray): input frame to find frame_size of
    return::
        frame_size (tuple): height and width of the input frame
    """
    frame_size = frame.shape[0],frame.shape[1]
    return frame_size

def dimensions(frame,returnType=0):
    """
    function which returns the dimensions and data_type of a given image

    input::
        frame (np.ndarray): image of which to find dimensions for
        returnType (str,bool): indicator that determine whether to return the
                            dimensions in a tuple or dictionary
    return::
        dimensions:
            if tuple: (rows, cols, bands, data_type)
            if dict: {"rows":rows,"cols":cols,"bands":bands,"dtype":data_type}
    """
    dimensions = frame.shape
    rows = dimensions[0]
    cols = dimensions[1]
    if len(dimensions) == 3:
        bands = dimensions[2]
    else:
        bands = 1
    data_type = frame.dtype
    if returnType in ["tuple","t",0]:
        return rows, cols, bands, data_type
    elif returnType in ["dictionary","dict","d",1]:
        return {"rows":rows,"cols":cols,"bands":bands,"dtype":data_type}







#END
