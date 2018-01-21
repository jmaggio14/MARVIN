import marvin
import cv2
import collections


class MultiCam(object):
    """
        object which is used to capture images from multiple cameras and stores them
        in an internal buffer for access by other processes
        input::
            cameras (list,tuple): list of ids for the openCV VideoCapture class, see marvin.CameraCapture
                    for more information
            cache_size (int): the number of frames to cache for each camera in the buffer
            fourccs (list): a list of fourcc strings to indicate which codec to use,
                            keep as None to use the default

        attributes::
            cam_ids (list): list of input camera ids, turned to strings
            buffer_size (int): input buffer_size, cast to an integer
            fourccs (list): list of strings, copied from input or if None, then
                        equal to ["MJPG"] * len(self.cam_ids)
            caps (list): list of marvin.CameraCapture objects for each camera, direct output
                        from __createCaptureObjects()
            buffers (list): list of marvin.CaptureBuffer objects, where the output from
                        each cameras is saved


        functions::
            __createCaptureObjects(): creates the marvin.CameraCapture objects used to
                        capture images from the camera
            __createBuffers(): creates the marvin.CaptureBuffer objects used to store
                        images off the cameras

        properties::
            None
    """
    def __init__(self,cameras,buffer_size=30,fourccs=None):
        self.buffer_size = int(buffer_size)


        if fourccs == None:
            fourccs = [None] * len(cameras)
        input_fourccs = fourccs

        #creating camera capture devices
        self.cam_ids,capture_devices = self.__createCaptureObjects(cameras,input_fourccs)

        self.caps = dict( zip(self.cam_ids,capture_devices) )
        #creating lists of valid camera ids and fourccs codes for each camera
        self.fourccs = []
        for cap in self.caps.values():
            self.fourccs.append( cap.fourcc )

        #creating the camera buffers
        self.buffers = self.__createBuffers(self.cam_ids,self.buffer_size)

        #creating a placeholder array for the FrameSets as a limited deque
        self.frame_sets = collections.deque( maxlen=self.buffer_size )

        self.set_number = 0

    def __createCaptureObjects(self,cameras,input_fourccs):
        """
            private to marvin.MultiCam

            creates the marvin.CameraCapture objects which will be used to talk to
            each individual camera
            input::
                None
            return::
                caps (dict): dict of marvin.CameraCapture objects created for each camera,
                            the key is the string of the corresponding cam_id
        """
        capture_devices = []
        cam_ids = []
        for i in range( len(cameras) ):
            cam = cameras[i]
            fourcc = input_fourccs[i]
            try:
                capture_devices.append( marvin.CameraCapture(cam,fourcc) )
                cam_ids.append( capture_devices[-1].cam_id )
                marvin.Status.info("adding CameraCapture object with input {0} with cam_id: {1} and fourcc {2}".format( cam,cam_ids[-1],capture_devices[-1].fourcc ))

            except marvin.MarvinCameraException:
                marvin.Status.critcal("unable to connect to camera: {0} with fourcc: {1}".format(cam,fourcc))

        return cam_ids,capture_devices

    def __createBuffers(self,cam_ids,buffer_size):
        """
        private to marvin.MultiCam

            creates the buffers necessary for temporary storage of frames
            input::
                None
            return::
                buffers (dict): dict of marvin.CaptureBuffer objects created for each
                                camera to store the frames in a temporarily available manner
                                the key is the corresponding cam_id
        """
        buffers = {}
        for cam_id in cam_ids:
            buffers[cam_id] = marvin.CaptureBuffer( buffer_size )
            marvin.Status.info("adding CaptureBuffer object for cam_id: {0}".format( cam_id ))
        return buffers

    def grab(self):
        """
            grabs frames off of each of the cameras and stores them in the appropriate buffer.
            it also generates a dictionary containing all the frame_ids of the frames
            grabbed (the keys are the frame's corresponding cam_id)

            input::
                None
            return::
                frame_set (dict): a dict which contains the
                        frame_ids of the frames that were grabbed. These values
                        are also stored in self.frame_sets
        """
        self.set_number += 1

        frame_ids = []
        for cam_id in self.cam_ids:
            frame = self.caps[cam_id].read()
            frame_ids.append( frame.id )
            self.buffers[cam_id].add( frame )

        frame_set = dict( zip(self.cam_ids,frame_ids) )
        self.frame_sets.appendleft( frame_set )
        return self.frame_sets[0]

    def retrieve(self,index_dict=None):
        """
            retrieves frames from each camera using an input dictionary to specify how
            to index into each camera. This makes for easy indexing into the array
            and allows for a arbitrary number of frames to be returned for each camera

            if index_dict is left as None, then the most recent frame from each camera is returned
            if index_dict is the string "all", then the all frames in the camera buffers will be returned
            if index_dict is an integer, then it will be treated as an index and will return that index for every buffer

            e.g.
                index_dict = {{"0":[0,1,2],
                                "1":[frame_id1,frame_id2],
                                "2":9,
                                "3":[15,frame_id3] }}

                retrieveFrames(index_dict)
                    --> returns:
                        a dictionary with the same keys containing:
                                "0":a list containing the first three frames off the buffer for camera "0"
                                "1":a list containing the frames specified by frame_id1 & frame_id2 for camera "1"
                                "2":the 10th frame off the buffer for camera "2"
                                "3": a list containing the 16th frame and the frame corresponding to frame_id3 for camera "3"


            input::
                index_dict (dict):
                    to return the first frame:
                        index_dict = None
                    to return all frames:
                        index_dict = "all"
                    to return all frames of a specific index in the buffer
                        index_dict = index
                    to return specific frames by cameras:
                        a dictionary which contains the frame_id, the index or
                        a list of either corresponding to the frames desired to be returned.
                        The keys for the above value should be the cam_id of the camera in question

                        a shortcut for this is the marvin.FrameSet class

            return::
                frames (dict): a dictionary containing the desired frames for each camera, or None
                    if those frames don't exist. the dictionary keys are the same as those for
                    the input index_dict or are the camera ids if index_dict is not a dict


            Note::
                review this code for additional error checking -- make custom exception
                for this purpose?
        """
        if index_dict == None:
            index_dict = dict( ( self.cam_ids, [0] * len(self.cam_ids) ) )
        elif index_dict == "all":
            index_dict = dict( zip( self.cam_ids, ["all"] * len(self.cam_ids) ))
        elif isinstance(index_dict,int):
            index_dict = dict( zip( self.cam_ids, [index_dict] * len(self.cam_ids) ))

        frames = {}
        for cam_id,key_index in index_dict.items():
            if cam_id in self.cam_ids:
                frames[cam_id] = self.buffers[cam_id][ key_index ]
                marvin.Status.debug("retrieving frame(s): {0} using index_dict: {1} on set_number: {2} from cam_id {3}".format(frames[cam_id].id,index_dict,self.set_number,cam_id))
            else:
                marvin.Status.warning("Unable to retrieve frame using index_dict: {0} on set_number: {1} from cam_id {2}".format(index_dict,self.set_number,cam_id))
                frames[cam_id] = None
        return frames


    #
    # def retrieveAllFrames(self):
    #     """
    #         retrieves all frames for each camera from the all camera buffers.
    #         equivalent of MultiCam.retrieve("all")
    #     """
    # def retrieveFramesUsingSetId(self,set_id):
    #     pass
    #
    # def retrieveFramesFromCamera(self,cam_id,key_index):
    #     """
    #     retrieves the a frame from a camera buffer identified by cam_id
    #     using an index, frame_id, or list of either
    #
    #     direct index into a camera buffer --> see CaptureBuffer.__getitem__ for
    #     more details
    #
    #     input::
    #         cam_id (marvin.CamId): the camera id of the buffer that the desired
    #         frames are from
    #         key_index (list,marvin.FrameId,int): the
    #
    #     """
    #     frames = self.buffers[cam_id][key_index]
    #     return frames
    #

    # def retrieveFrameSetIndexFromFrameId(self,frame_id):
    #     pass
    #
    # def retrieveFrameSetIndexFromSetId(self,frame_id):
    #     pass


#END
