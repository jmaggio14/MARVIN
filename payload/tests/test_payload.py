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
# from . import
from marvin.payload import Payload

def test_payload():
    """unit test for the Payload Class"""

    # Creating two unique test payloads
    print("Creating two unique test payloads")
    payload1 = Payload("payload1")
    payload2 = Payload("payload2")

    # checking validity of payload name assignment
    print("checking validity of name assignment")
    if payload1.get_payload_name() != "payload1":
        print("name assignment failure")
        return False
    if payload2.get_payload_name() != "payload2":
        print("name assignment failure")
        return False

    # attempting to create a third payload with an invalid name
    # print("creating a 3rd payload with an invalid name")
    # try:
    #     invalid_payload = Payload("payload1")
    #     print("creation of payload")
    # except ValueError:
    #     print("creation of invalid payload was denied successfully")
    # except:
    #     print("AN UNEXPECTED EXCEPTION OCCURED")
    #     return -1

    return True
