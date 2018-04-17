#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#

##------------------ function Tests -------------------------
def test__calculate_centroid():
    """
    tests the calculate_centroid function
    input::
        None
    returns::
        ret(bool):
            whether or not the test was passed
    """
    import numpy as np
    import marvin
    test_array = np.ones(7,102)
    centroid = marvin.calculate_centroid(test_array)
    if centroid == (3,51):
        ret = True
    else:
        ret = False
    return ret


def test__calculate_frame_size():
    """
    tests the calculate_frame_size function
    input::
        None
    returns::
        ret(bool):
            whether or not the test was passed
    """
    import numpy as np
    import marvin
    test_array = np.ones(7,102,3,3)
    frame_size = marvin.calculate_frame_size(test_array)
    if frame_size == (7,102):
        ret = True
    else:
        ret = False
    return ret



def test__get_image_dimensions():
    """
    tests the get_image_dimensions function
    input::
        None
    returns::
        ret(bool):
            whether or not the test was passed
    """
    import numpy as np
    import marvin
    test_array = np.ones(7,102,3,3).astype(np.uint8)
    dimensions = marvin.get_image_dimensions(test_array)
    if dimensions == (7,102,3,np.uint8):
        ret = True
    else:
        ret = False
    return ret




## ------------------- OBJECT TESTS -----------------
def test__Frame():
    """
    tests the marvin Frame object
    input::
        None
    returns::
        ret(bool):
            whether or not the test was passed
    """
    import marvin
    import numpy as np

    #building the frame
    test_array = np.ones(512,512)
    frame_id = "-1:-100"
    metadata = {"gain":1.0,"contrast":.5,"fps":30}
    frame = marvin.imtoolkit.Frame(test_array,frame_id,metadata)

    if hasattr(frame,"metadata"):
        gain = frame.metadata["gain"]
        contrast = frame.metadata["contrast"]
        fps = frame.metadata["fps"]

    if (gain == 1.0) and (contrast == 0.5) and (fps == 30):
        attrs_okay = True
    else:
        attrs_okay = False

    inheritance_okay = isinstance(frame,np.ndarray)

    ret = attrs_okay and inheritance_okay
    return ret






#END
