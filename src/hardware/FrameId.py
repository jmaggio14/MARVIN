import marvin


class FrameId(str):
    """
    a string constructor class that generates an frame_id string from a camera id
    and a frame_number

    input::
        cam_id (int,str): the camera id
        frame_number (int,str): the frame number

    attribute::
        cam_id (str): the camera id
        frame_number (int): the frame number as an integer

    """
    def __new__(cls,cam_id=-1,frame_number=-1,num_digits=7):
        cam_id = str( cam_id )
        frame_number = int( frame_number )
        num_digits = int( num_digits )
        frame_id = "{0}:{1}".format(cam_id, marvin.fileNumber(frame_number,num_digits) )
        return str.__new__(cls,frame_id)

    def __init__(self,cam_id=-1,frame_number=-1,num_digits=7):
        self.cam_id = marvin.CamId( cam_id )
        self.frame_number = frame_number

# class SetId(str):
#     """
#     a string constructor class that generates a set id from a set_number
#
#     input::
#         set_number (int,str): the number of the set
#     """
#     def __new__(cls,set_number=-1):
#         return str.__new__(cls, marvin.fileNumber( int(set_number) ),4 )


class CamId(str):
    """
    A string constructor that constructs a cam_id from the filename or UVC camera
    index ( the last number in /dev/video# )

    input::
        cam (str,int): the string of the UVC file index or the filename of the video
    """
    def __new__(cls,cam):
        return str.__new__(cls, cam )





# END
