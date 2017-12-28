import marvin


class CaptureBuffer(object):
    """
    An object meant to buffer an array of marvin.FrameContainer objects for later retrieval
    These buffers are designed to be used in a last in - first out design, but
    have the ability to retreive a frame using it's id or index into the buffer

    input::
        buffer_size (int): the number of frames to be stored in the buffer

    attributes::
        buffer_size (int): input buffer size cast to an int
        buffer (dict): a dictionary which stores the frame containers with the frame id as the key
        order (list): a list of frame ids which indicates the order of the frames in the buffer
                structured [NEWEST_ID, ..., OLDEST_ID] (oldest id is at the end of the list)

    functions::
        add(frame): adds an frame to the buffer, deletes old ones as necessary
        getNewest(): returns the newest frame off the buffer
        getOldest(): returns the oldest frame off the buffer
        getAll(): returns all frames off the buffer
        getByList(index_list): returns a list of frames defined by an input list
        getByIndex(index): returns a frame according an index into the buffer
        getByID(frame_id): returns a frame according a frame_id index


    properties::
        None

    """
    def __init__(self,buffer_size):
        self.buffer_size = int(buffer_size)
        self.buffer = {}
        self.order = []

    def add(self,frame):
        """
        adds a frame to the buffer and updates the self.order list. if the buffer
        becomes larger than the specified buffer size, then the oldest value is deleted

        input::
            frame: marvin.FrameContainer object of the input image
        return::
            None
        """
        if isinstance(frame,marvin.FrameContainer):
            self.buffer[frame.id] = frame
            #insert the value at the beginning of the order
            self.order.insert(0,frame.id)

        if len(self.buffer) > self.cache_size:
            oldest_id = self.order[-1]
            #deleting the last value in the buffer and the corresponding value in self.order
            del( self.buffer[oldest_id] )
            del( self.order[-1] )

    def getNewest(self):
        """
        grabs the newest frame off the buffer, ie the most recent one added to the buffer

        input::
            None
        return::
            newest (marvin.FrameContainer): the most recent frame off the buffer
        """
        newest = self.getByIndex(0)
        return newest


    def getOldest(self):
        """
        grabs the oldest frame off the buffer, ie the least recent one in the buffer

        input::
            None
        return::
            oldest (marvin.FrameContainer): the oldest frame off the buffer
        """
        oldest = self.getByIndex(-1)
        return oldest


    def getAll(self):
        """
        returns all the frames in the buffer in order of newest-->oldest

        input::
            None
        frames::
            frames (list):: list of all marvin.FrameContainer objects
        """
        frames = self.getByList( self.order )
        return frames


    def getByList(self,index_list):
        """
        this function will treat each value in this list as an index or frame_id into the buffer
        returns a list of frames of equal length to 'input1', None if id or index doesn't not exist

        input::
            index_list: list of indices to parse and retrieve frames for
        return::
            frames (list): list of frames, retrieved by index or id
        """
        frames = []
        for i in index_list:
            if isinstance(i,int):
                frames.append( self.__getByIndex(i) )

            elif isinstance(i,str):
                frames.append( self.__getByID(i) )

            else:
                marvin.Status.warning("unable to use indexing type '{0}' for getByList(), appending None to output".format( type(i) ) )
                frames.append(None)

        return frames


    def getByIndex(self,index):
        """
        retrieves the frame defined by an index value into the buffer
        e.g.
            getByIndex(9) --> returns the 10th frame off the buffer (self.buffer[index])

        input::
            index (int): the index into the buffer
        return::
            frame (marvin.FrameContainer,None): the frame at self.buffer[ self.order[index] ]
        """
        try:
            frame_id = self.order[index]
            return self.__getByID(frame_id)
        except IndexError:
            marvin.Status.warning( "INVALID INDEX: {0} for indexing into buffer".format(index) )
            return None


    def getByID(self,frame_id):
        """
        retrieves the associated with that frame_id in the buffer
        e.g.
            getByID("0:27") --> returns the frame with the id "0:27"

        input::
            frame_id (str): the frame id of the frame to be indexed
        return::
            frame (marvin.FrameContainer,None): the frame at self.buffer[frame_id]
        """
        try:
            frame = self.buffer[frame_id]
            return frame
        except KeyError:
            marvin.Status.warning( "INVALID FRAME ID: {0} for indexing into buffer".format(frame_id) )
            return None
