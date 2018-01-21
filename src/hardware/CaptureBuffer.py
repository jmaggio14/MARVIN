import marvin


class CaptureBuffer(object):
    """
    An object meant to buffer an array of marvin.Frame objects for later retrieval
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
        getByList(index_key_list): returns a list of frames defined by an input list
        getByIndex(index): returns a frame according an index into the buffer
        getByID(frame_id): returns a frame according a frame_id index

    properties::
        None

    operators::
        __getitem__(key): retrieves the desired frame from the buffer using a frame_id,
                        index, or list of either
    """
    def __init__(self,buffer_size=30):
        self.buffer_size = int(buffer_size)
        self.buffer = {}
        self.order = []

    def add(self,frame):
        """
        adds a frame to the buffer and updates the self.order list. if the buffer
        becomes larger than the specified buffer size, then the oldest value is deleted

        input::
            frame: marvin.Frame object of the input image
        return::
            frame_id (str): the id of the frame at the beginning of the buffer (self.order[0])
        """
        if isinstance(frame,marvin.Frame):
            self.buffer[frame.id] = frame
            #insert the value at the beginning of the order
            self.order.insert(0,frame.id)

        if len(self.buffer) > self.buffer_size:
            oldest_id = self.order[-1]
            #deleting the last value in the buffer and the corresponding value in self.order
            del( self.buffer[oldest_id] )
            del( self.order[-1] )

        return self.order[0]

    def getNewest(self):
        """
        grabs the newest frame off the buffer, ie the most recent one added to the buffer

        input::
            None
        return::
            newest (marvin.Frame,marvin.DebugImage): the most recent frame off the buffer
        """
        newest = self.getByIndex(0)
        return newest


    def getOldest(self):
        """
        grabs the oldest frame off the buffer, ie the least recent one in the buffer

        input::
            None
        return::
            oldest (marvin.Frame,marvin.DebugImage): the oldest frame off the buffer
        """
        oldest = self.getByIndex(-1)
        return oldest


    def getAll(self):
        """
        returns all the frames in the buffer in order of newest-->oldest

        input::
            None
        frames::
            frames (list):: list of all marvin.Frame objects ordered newest to oldest
        """
        frames = self.getByList( self.order )
        return frames


    def getByList(self,index_key_list):
        """
        this function will treat each value in this list as an index or frame_id into the buffer
        returns a list of frames of equal length to 'input1', None if id or index doesn't not exist

        input::
            index_key_list (list,tuple): list of indices to parse and retrieve frames for
        return::
            frames (list): list of frames, retrieved by index or id
        """
        frames = []
        for i in index_key_list:
            if isinstance(i,int):
                frames.append( self.__getByIndex(i) )

            elif isinstance(i,str):
                frames.append( self.__getByID(i) )

            else:
                debug_message = "unable to use index/key type '{0}' for getByList(), appending None to output".format( type(i) )
                marvin.Status.warning( debug_message )
                frames.append(None)
                # frames.append( marvin.DebugImage( debug_message ) )

        return frames


    def getByIndex(self,index):
        """
        retrieves the frame defined by an index value into the buffer
        e.g.
            getByIndex(9) --> returns the 10th frame off the buffer

        input::
            index (int): the index into the buffer
        return::
            frame (marvin.Frame,marvin.DebugImage): the frame at self.buffer[ self.order[index] ]
        """
        try:
            frame_id = self.order[index]
            return self.getByID( frame_id )
        except IndexError:
            debug_message = "INVALID INDEX: {0} for indexing into capture buffer".format(index)
            marvin.Status.warning( debug_message )
            # return marvin.DebugImage(message=debug_message)
            return None


    def getByID(self,frame_id):
        """
        retrieves the associated with that frame_id in the buffer
        e.g.
            getByID("0:0027") --> returns the frame with the id "0:0027"

        input::
            frame_id (str): the frame id of the frame to be indexed
        return::
            frame (marvin.Frame,marvin.DebugImage): the frame at self.buffer[frame_id]
        """
        try:
            frame = self.buffer[frame_id]
            marvin.Status.debug("returning frame: {0} from the buffer at index: {1}".format(frame.id,self.getIndexOfFrameId(frame.id)))
            return frame
        except KeyError:
            debug_message = "INVALID FRAME ID: {0} for indexing into buffer. valid ids are {1}".format(frame_id,self.buffer.keys())
            marvin.Status.warning( debug_message )
            # return marvin.DebugImage( debug_message )
            return None


    def getIndexOfFrameId(self,frame_id):
        """
        Retrieves the index of a frame_id off of the buffer, if the frame corresponding
        to that frame_id doesn't exist in the buffer, then None is returned

        input::
            frame_id (marvin.FrameId): the input frame_id
        return::
            index (None,int): The index of the frame_id in the buffer, or None if it
            doesn't exist

        Note::
            It may be more prudent to raise a custom marvinException instead of
            returning None
        """
        if frame_id in self.order:
            index = self.order.index(frame_id)
        else:
            marvin.Status.warning( "frame_id: {0} does not exist in this buffer".format( frame_id ) )
            index = None

        return index

    def __getitem__(self,key_index):
        """
        overloads the __getitem__ operator so the buffer can be indexed without
        special functions
        e.g.
            capture_buffer[frame_id] --> returns capture_buffer.getByID(frame_id)
            capture_buffer[0] --> returns capture_buffer.getByIndex(0)

        input::
            key_index (str,int,list): key, index or list of either to index into the buffer
        return::
            frame (list,marvin.Frame,marvin.DebugImage): the frame(s) at the index location(s)
        """
        if key_index == "all":
            return self.getAll()

        if isinstance(key_index,marvin.FrameId):
            return self.getByID( key_index )

        elif isinstance(key_index,int):
                return self.getByIndex( key_index )

        elif isinstance(key_index,(list,tuple)):
                return self.getByList( key_index )

        else:
            debug_message = "INVALID KEY/INDEX: {0} for indexing into capture buffer".format( key_index )
            marvin.Status.warning( debug_message )
            # return marvin.DebugImage( debug_message )
            return None


    @property
    def frame_ids(self):
        """
        returns the self.order attribute
            `--> ie an ordered list of frame_ids in the buffer
        """
        return self.order
