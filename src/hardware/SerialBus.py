import serial
import marvin

class MarvinSerialBus(serial.Serial):
    """
    class which inherits from pyserial's serial.Serial
    https://pythonhosted.org/pyserial/

    This is meant to be used to talk to devices over a uart or serial connection


    """
    def __init__(self,*args,**kwargs):
        super(SerialBus,self).__init__(*args,**kwargs)
        self._termination_char = "\n"

    def command(command="\n"):
        """
        encodes and writes a given string to the

        automatically adds a termination character (usually a newline) if one
        doesn't already exist

        automatically catches
        """
        #adding a termination character if it's needed
        if command[-1] != "\n": command+=self.termination_char
        #converting to ascii if not already in the correct form
        if not isinstance(command,bytes):
            command = bytes(command,encoding="ascii")

        try:
            self.write(command)
        except serial.serialutil.SerialException:
            raise marvin.MarvinSerialException



    @property
    def termination_char(self):
        return termination_char
    @termination_char.setter
    def termination_char(self,termination_char):
        self._termination_char = termination_char
