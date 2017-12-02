
import logging
import os
import marvin
import threading
import time

class PwmController(threading.Thread,DigitalPin):
    """
    class which oscillates a digital pin on and off in an attempt to mimic a true
    pwm controller.

    This would be vastly more efficient if compiled in C and merely called in
    python

    inherits from marvin.DigitalPin and threading.Thread


    unique attributes::
        duty_cycle (float): fraction of time signal is on (the average)
        period (float): duty cycle period (temporal-wavelength) in microseconds
        _on_time (float): time square wave is 1
        _off_time (float): time square wave is 0

    functions::
        setup: calculates time on and off, resets duty_cycle and period
        run: function is continuously run on new thread

    """
    def __init__(self,pin_number,duty_cycle,period=100,**kwargs):
        self.duty_cycle = float(duty_cycle)
        self.period = float(period)
        self.kwargs = kwargs
        DigitalPin.__init__(pin_number,direction=marvin.GPIO_OUTPUT,**kwargs)
        threading.Thread.__init__()
        self.setup(self.duty_cycle,self.period)

    def setup(self,duty_cycle=None,period=None):
        if not isinstance(period,type(None)): self.period = period
        if not isinstance(duty_cycle,type(None)): self.duty_cycle = duty_cycle
        self._on_time = (self.duty_cycle * self.period) / 1e6
        self._off_time = ((1.0-self.duty_cycle) * self.period ) / 1e6

    def run(self):
        self.value = 1
        time.sleep(self._on_time)
        self.value = 0
        time.sleep(self._off_time)


class DigitalPin(object):
    """
    Class built to simplify the operation of GPIO (General Purpose Input Output)
    pins in embedded linux systems. it relies GPIO pins being accessible at
    '/sys/class/gpio/' (which, to the author's knowledge, is universal)

    This class may have to be run with 'sudo' to properly access gpio files!
    (keep in mind that this can potentially be a significant security flaw,
    especially if you run this in a script that has networking elements)

    This class only operates on digital pins and does not have PWM functionality
    built in.


    for the Jetson Tk1, useable pins are as follows:
        [57,160,161,162,163,164,165,166]


    input::
        pin_number (int,str): the pin number to be toggled
        direction (str,marvin.CONSTANT): the direction of the pin in question
            this must be either marvin.GPIO_INPUT or marvin.GPIO_OUTPUT

    functions::
        checkPin: checks the pin to determine if it's still exported
        toggleOn: sets value to 1
        toggleOff: sets value to 0
        unexport: unexports pin
        export: exports pin
        invertLogic: inverts the value of active_low

    properties::
        direction:
            getter: retrieves the current pin direction
            setter: resets the pin direction
        value:
            getter: retrieves the current value of the pin, this works for input and output pins
            setter: sets the pin direction, either marvin.GPIO_INPUT or marvin.GPIO_OUTPUT
        active_low:
            getter: retrieves a value of the active_low boolean
            setter: sets the active_low state
    """
    def __init__(self,pin_number,direction=None,active_low=0):
        if isinstance(direction,type(None)): direction=GPIO_INPUT
        self.pin_number = str(pin_number)
        #error checking the direction
        if direction not in [marin.GPIO_INPUT,marvin.GPIO_OUTPUT]:
            marvin.Status.warning("invalid GPIO pin direction, must be '{in}' or '{out}'".format( **{"in":marvin.GPIO_INPUT,"out":marvin.GPIO_OUTPUT} ) )
            marvin.Status.warning("setting GPIO as default value (input)")
            direction = marvin.GPIO_INPUT

        self.export(direction)
        self.direction = direction
        self.active_low = active_low

    def checkPin(self):
        """
        checks to see if a pin is exported
        input::
            None
        return::
            export_status (bool): boolean indicating whether or not the pin is exported
        """
        #checking to see if the pin number is invalid
        if os.path.exists('/sys/class/gpio/export/gpio' + self.pin_number):
            export_status = True
        else:
            marvin.Status.critical("unable to export GPIO pin! does pin exist?")
            export_status = False
        return export_status

    def toggleOn(self):
        """
        shortcut function to set the value to 1
        input::
            None
        return::
            None
        """
        self.value = 1

    def toggleOff(self):
        """
        shortcut function to set the value to 0
        input::
            None
        return::
            None
        """
        self.value = 0

    def unexport(self):
        """
        unexports the pin, the pin will be unuseable unless it is re-exported
        input::
            None
        return::
            None
        """
        with open('/sys/class/gpio/unexport','w') as unexport_file:
            if not os.path.exists('/sys/class/gpio/unexport/gpio' + self.pin_number):
                export_file.write( self.pin_number )

    def export(self,direction):
        """
        exports the pin, this makes the pin useable
        input::
            direction (str,marvin.CONSTANT): the pin direction, either marvin.GPIO_INPUT, marvin.GPIO_OUTPUT
        return::
            None
        """
        with open('/sys/class/gpio/export','w') as export_file:
            if not os.path.exists('/sys/class/gpio/export/gpio' + self.pin_number):
                export_file.write( self.pin_number )


    def invertLogic(self):
        """
        inverts the current logic settings (determines whether the pin is active_low or active_high)
        input::
            None
        return::
            None
        """
        active_low = self.active_low
        self.active_low = not active_low


    @property
    def value(self):
        """
        retrieves the value from the direct GPIO file

        returns nothing if pin is not exported
        input::
            None
        return::
            value(bool): the state of the pin (either 1 or 0)
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/value'.format( self.pin_number ),'r') as value_file:
                value = bool( value_file.read() )
            return value
        else:
            return None
    @value.setter
    def value(self,value):
        """
        writes the given value to the GPIO value file

        does nothing if pin is not exported

        input::
            value (int,bool): the value you want to set on the pin (either 1 or 0)
        return::
            None
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/value'.format( self.pin_number ),'w') as value_file:
                value_file.write( bool(value) )

    @property
    def direction(self):
        """
        retrieves the current direction directly from the GPIO file
        input::
            None
        return::
            direction (str,marvin.CONSTANT): the pin direction, either marvin.GPIO_INPUT, marvin.GPIO_OUTPUT
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/direction'.format( self.pin_number ),'r') as direction_file:
                direction = direction_file.read()
            return direction
        else:
            return None
    @direction.setter
    def direction(self,direction):
        """
        writes the given value to the GPIO direction file
        input::
            direction (str,marvin.CONSTANT): the pin direction, either marvin.GPIO_INPUT, marvin.GPIO_OUTPUT
        return::
            None
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/direction'.format( self.pin_number ),'w') as direction_file:
                direction_file.write( direction )

    @property
    def active_low(self):
        """
        retrieves the current active_low state directly from the GPIO file
        input::
            None
        return::
            active_low (bool): the current active_low state in boolean form
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/active_low'.format( self.pin_number ),'r') as active_low_file:
                active_low = bool(active_low_file.read())
            return active_low
        else:
            return None
    @active_low.setter
    def active_low(self,active_low):
        """
        writes the  value to the active_low file
        input::
            active_low: the active_low value, either 0 or 1
        return::
            None
        """
        if self.checkPin():
            with open('/sys/class/gpio/gpio{0}/active_low'.format( self.pin_number ),'w') as active_low_file:
                active_low_file.write( str(active_low) )
