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
"""
CONSTANTS::
    GPIO::
        GPIO_INPUT = "in"
        GPIO_OUTPUT = "out"
        GPIO_ON = 1
        GPIO_OFF = 0
    LOGGER::
        LOGGER_STATUS = 0
        LOGGER_EVENT = 1
        LOGGER_PRIORITY_LEVEL = 60
    GSTEAMER::
        GSTREAMER_ENCODER_X264 = "x264enc"
        GSTREAMER_ENCODER_OMX264 = "omx264enc"
"""
#GPIO CONSTANTS
GPIO_INPUT = "in"
GPIO_OUTPUT = "out"
GPIO_HIGH = 1
GPIO_LOW = 0


#LOGGER CONSTANTS
LOGGER_STATUS = 0
LOGGER_EVENT = 1
LOGGER_PRIORITY_LEVEL = 60


#GSTREAMER CONSTANTS
GSTREAMER_ENCODER_X264 = "x264enc"
GSTREAMER_ENCODER_OMX264 = "omx264enc"


#Standard type tables (for error checking)
NUMPY_TYPES =( np.uint8,
				np.int8,
				np.uint16,
				np.int16,
				np.int32,
				np.float32,
				np.float64,
				np.complex64,
				np.complex128 )
