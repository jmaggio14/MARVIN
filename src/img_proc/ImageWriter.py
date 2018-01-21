import marvin
import cv2


class ImageWriter(object):
    """
    Class that operates as a system that saves single frames to a specied output
    directory
    __init__ input::
        output_dir (str): path to output directory that images will be saved to
        base_filename (str): filename common among all images
        size (tuple,None): size of the image if forced resizing is desired, or
                    NoneType if raw write is desired
        interpolation (cv2 interpolation type): interpolation method to be used if resizing is desired


    functions::
        write():
            writes a frame with a unique filename to the specificed image directory
            input::
                frame (np.ndarray): input frame to be saved
            return::
                None
    """
    def __init__(self,output_dir,base_filename="image.png",size=None,interpolation=cv2.INTER_NEAREST):
        self.output_dir = marvin.preventOverwrite(output_dir,create_file=True)
        self.base_filename = base_filename
        self.size = size
        self.interpolation = interpolation
        self.image_number = 0

    def write(self,frame):
        """
        writes an image frame to the specificed directory, forces resizing if
        specified when the class is instantiated
        input::
            frame (np.ndarray): frame to be saved to the output directory
        return::
            None
        """
        self.image_number += 1
        filename = marvin.preventOverwrite(self.output_dir + marvin.fileNumber(self.image_number) + self.base_filename)

        if not isinstance(self.size,type(None)):
            frame = cv2.resize(frame,(self.size[1],self.size[0]),interpolation=self.interpolation)

        cv2.imwrite(filename,frame)



if __name__ == "__main__":
    try:
        marvin.init()
        print(
        """
        testing the ImageWriter
            output_dir:{0}
            base_filename:{1}
            size:{2}
            interpolation:{3}

        This test relies on a camera being attached to /dev/video0 and
        marvin.CameraCapture being operational
        """.format( "output/ImageWriterTest/","testImage.png",None,cv2.INTER_AREA )
        )
        timer = marvin.Timer()
        cap = marvin.CameraCapture(0)
        viewer = marvin.Cv2ImageViewer("image writer test")
        image_writer = marvin.Cv2ImageWriter("output/ImageWriterTest/")
        timer.countdown = 10
        while timer.countdown:
            frame = cap.read()
            viewer.view(frame)
            image_writer.write(frame)
    except Exception as e:
        marvin.debug(e)




#END
