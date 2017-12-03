import logging
import os
import marvin
import threading
import time

# class Python_PwmController(threading.Thread,marvin.DigitalPin):
#     """
#     class which oscillates a digital pin on and off in an attempt to mimic a true
#     pwm controller.
#
#     This would be vastly more efficient if compiled in C and merely called in
#     python
#
#     inherits from marvin.DigitalPin and threading.Thread
#
#
#     unique attributes::
#         duty_cycle (float): fraction of time signal is on (the average)
#         period (float): duty cycle period (temporal-wavelength) in microseconds
#         _on_time (float): time square wave is 1
#         _off_time (float): time square wave is 0
#
#     functions::
#         setup: calculates time on and off, resets duty_cycle and period
#         run: function is continuously run on new thread
#
#     """
#     def __init__(self,pin_number,duty_cycle,period=100,**kwargs):
#         self.duty_cycle = float(duty_cycle)
#         self.period = float(period)
#         self.kwargs = kwargs
#         self.setup(self.duty_cycle,self.period)
#         DigitalPin.__init__(pin_number,direction=marvin.GPIO_OUTPUT,**kwargs)
#         threading.Thread.__init__()
#
#     def setup(self,duty_cycle=None,period=None):
#         if not isinstance(period,type(None)): self.period = period
#         if not isinstance(duty_cycle,type(None)): self.duty_cycle = duty_cycle
#         self._on_time = (self.duty_cycle * self.period) / 1e6
#         self._off_time = ((1.0-self.duty_cycle) * self.period ) / 1e6
#
#     def run(self):
#         while True:
#             self.value = 1
#             time.sleep(self._on_time)
#             self.value = 0
#             time.sleep(self._off_time)
#
# # class C_PwmController(object):
# #
# #
# # class PwmController(threading.Thread,DigitalPin):
# #     """
#     class which oscillates a digital pin on and off in an attempt to mimic a true
#     pwm controller.
#
#     This would be vastly more efficient if compiled in C and merely called in
#     python
#
#     inherits from marvin.DigitalPin and threading.Thread
#
#
#     unique attributes::
#         duty_cycle (float): fraction of time signal is on (the average)
#         period (float): duty cycle period (temporal-wavelength) in microseconds
#         _on_time (float): time square wave is 1
#         _off_time (float): time square wave is 0
#
#     functions::
#         setup: calculates time on and off, resets duty_cycle and period
#         run: function is continuously run on new thread
#
#     """
#     def __init__(self,pin_number,duty_cycle,period=100,**kwargs):
#         self.duty_cycle = float(duty_cycle)
#         self.period = float(period)
#         self.kwargs = kwargs
#         DigitalPin.__init__(pin_number,direction=marvin.GPIO_OUTPUT,**kwargs)
#         threading.Thread.__init__()
#         self.setup(self.duty_cycle,self.period)
#
#     def setup(self,duty_cycle=None,period=None):
#         if not isinstance(period,type(None)): self.period = period
#         if not isinstance(duty_cycle,type(None)): self.duty_cycle = duty_cycle
#         self._on_time = (self.duty_cycle * self.period) / 1e6
#         self._off_time = ((1.0-self.duty_cycle) * self.period ) / 1e6
#
#     def run(self):
#         self.value = 1
#         time.sleep(self._on_time)
#         self.value = 0
#         time.sleep(self._off_time)
