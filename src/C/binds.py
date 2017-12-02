import ctypes

"""
This is not the most robust way for large C bindings. but it works well for the
quick simple C functions we are working with

to bind code using this system:

1) you must compile the C code into a '.so' shared library
    $ gcc -o NAME_OF_LIBRARY.so -shared -fPIC NAME_OF_C_FILE.c

2) import ctypes
    >>> import ctypes

3) retrieve the shared library
    >>> NAME_OF_LIBRARY = ctypes.cdll.LoadLibrary("NAME_OF_LIBRARY.so")

4) pull out the function you want to bind
    >>> FUNCTION_NAME = NAME_OF_LIBRARY.FUNCTION_NAME

5) define the ctype you want to return from this function
    >>> FUNCTION_NAME.restype = ctypes.<ctype c_Type you want to return>

a full example is below:

                C Code
---------------------------------------
#include <stdlib.h>

int testFunc(int input1){
  if (input1>10){
    return input1;
  }
  else{
    return 0;
  }
}


            compilation command
--------------------------------------
$ gcc -o test_lib.so -shared -fPIC test.c



            python binding code
---------------------------------------
c_test_lib = ctypes.cdll.LoadLibrary("test_lib.so")
#this is where the function is actually created
c_testFunc = c_test_lib.testFunc
c_testFunc.restype = ctypes.c_uint

            python wrapper
----------------------------------------
I reccommend additionally wrapping the bound methods in a function that will force
type conversion, this will make for cleaner code later and will idiot proof
things for to a certain degree.
(It's easy to get lazy with types when you are working in such a nice language
like python)-- anyone that's worked in C knows how frustrating type mismatches
can be :P

def testFunc(input1):
    '''
    wrapper for c_testFunc to force correct type conversion
    input::
        input1(int): a number
    return::
        out(int): input1 if input1 > 10, else 0
    '''
    input1 = ctypes.c_uint(input1)
    out = ctypes.c_int( c_testFunc(input1) ).value
    return out

            test harness
---------------------------------------
if __name__ == "__main__":
    print("testing 'testFunc' binding...")
    print("this should be 0: ",testFunc(5))
    print("this should be -50: ",testFunc(-50))


for more help, see:
https://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html
"""
#
# c_test_lib = ctypes.cdll.LoadLibrary("test_lib.so")
# c_testFunc = c_test_lib.testFunc
# c_testFunc.restype = ctypes.c_uint
#
#
# def testFunc(input1):
#     """
#     wrapper for c_testFunc to force correct type conversion
#     input::
#         input1(int): a number
#     return::
#         out(int): input1 if input1 > 10, else 0
#     """
#     input1 = ctypes.c_uint(input1)
#     out = ctypes.c_int( c_testFunc(input1) ).value
#     return out


c_pwm_lib = ctypes.cdll.LoadLibrary("pwm.so")
c_pulseWidthModulation = c_pwm_lib.pulseWidthModulation
c_pulseWidthModulation.restype = ctypes.c_int

def pulseWidthModulation(pin_number,on_time,off_time):
    """
    python wrapper for the C function c_pulseWidthModulation
    input::
        pin_number(int): pin number for GPIO

        #INCOMPLETE
    """

    pin_number = ctypes.c_int(pin_number)
    on_time = ctypes.c_uint(on_time)
    off_time = ctypes.c_uint(off_time)

    c_res = c_pulseWidthModulation(pin_number,on_time,off_time)
    res = ctypes.c_int(c_res).value
    return res

if __name__ == "__main__":
    print("testing pulseWidthModulation binding... NOT FULL PWM TEST")
    a = pulseWidthModulation(57,10,10)
    print("this should be 1:",a)
