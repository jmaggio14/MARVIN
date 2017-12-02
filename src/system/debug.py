import numpy as np
import sys
import os
import traceback
import inspect


def currentLineno():
    """
    returns the linenumber of the line that calls this function
    input::
        None
    return::
        linenumber of the last frame (the frame that calls this function)
    """
    cf = inspect.currentframe()
    return cf.f_back.f_lineno
def currentFile():
    cf = inspect.currentframe()
    return cf.f_back.co_filename


def outerLineno():
    """
    returns the linenumber of the call that called of this function
    input::
        None
    return::
        linenumber 2 frames back (the linenumber that called the function that called this function )
    """
    cf = inspect.currentframe()
    return cf.f_back.f_back.f_lineno
def outerFile():
    cf = inspect.currentframe()
    return cf.f_back.f_back.co_filename


def outerLineno2():
    """
    returns the linenumber of the line that called the line that called the line that called this function
    (3 frames back)
    input::
        None
    return::
        line number 3 frames back
    """
    cf = inspect.currentframe()
    return cf.f_back.f_back.f_back.f_lineno
def outerFile2():
    cf = inspect.currentframe()
    return cf.f_back.f_back.f_back.co_filename

def outerLinenoN(N):
    """
    returns the line number N frames back
    input::
        N -- number of frames back
    return::
        line number of the frame N frames back
    """
    frame = inspect.currentframe()
    for i in range(N):
        frame = frame.f_back
    return frame.f_lineno
def outerFileN():
    frame = inspect.currentframe()
    for i in range(N):
        frame = frame.f_back
    return frame.co_filename

def debug(exception,raise_system_exit=True,message=""):
    if message != "": "\r\n\r\nNote: "+message
    f = outerFile()
    lineno = outerLineno()
    exc_type,_,tb = sys.exc_info()
    traceback.print_tb(tb)
    print(
"""
===============================================================
                    |  initital traceback  |
file: {0}
lineno: {1}
type: {2}

exception: {3} {4}
===============================================================
""".format(f,lineno,exc_type,exception,message)
)
    if raise_system_exit:
        raise SystemExit


def typeCheck(var,types):
    if not isinstance(types,(tuple,list)): types = tuple(types)
    if isinstance(var,types):
        return True
    else:
        return False

def boundaryCheck(var,boundaries,var_name="var",inclusive=True):
    low_val = boundaries[0]
    high_val = boundaries[1]
    if low_val == None: low_val = -float('inf')
    if high_val == None: high_val = float('inf')

    if inclusive:
        if var <= boundaries[1]:high_ok = True
        else: high_ok = False
        if var >= boundaries[0]: low_ok = True
        else: low_ok = False
    else:
        if var < boundaries[1]: high_ok = True
        else: high_ok = False
        if var > boundaries[0]: low_ok = True
        else:low_ok = False
    return low_ok and high_ok

if __name__ == "__main__":
    print("boundaryCheck check not inclusive")
    a = boundaryCheck(5,(5,50),"5",False)
    print(a)
    print("boundaryCheck check inclusive")
    a = boundaryCheck(5,(5,50),"5",True)
    print(a)
    def test():
        try:
            raise TypeError
        except Exception as e:
            debug(e,"test")
    test()
# def debug(exception):

# 	"""
# 	simple method to remove unecessary clutter in debugging
# 	meant to be called exclusively in a try statement
#
# 	simply prints the file,line and exeption has occured in more organized
# 	and easily readable fashion
# 	"""
# 	exc_type, exc_obj, tb = sys.exc_info()
# 	fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]
# 	line = tb.tb_lineno
# 	traceback.print_tb(tb)
#     # print(
#     # """
#     # ===============================================================
#     #                     | initital traceback |
#     # file: {0}
#     # line: {0}
#     #
#     # ===============================================================
#     # """
#     # )
#
#     print("===============================================================")
# 	print("\r\n")
# 	print("                   | initital traceback | ")
# 	print("file: {0}\r\n\r\nline: {1} \r\n\r\ntype: {2}\r\n\r\n{3}\r\n".format(fname,line,exc_type,exception))
# 	print("===============================================================")
# 	raise SystemExit
# #
#
#
# def type_check(var,types,varName="var"):
# 	types = tuple(types) if isinstance(types,list) else types
# 	if isinstance(var,types) == False:
# 		print("-----------------------------------------------------------")
# 		print("-----------------------------------------------------------")
# 		print("                       TYPE ERROR                       \n")
# 		print("'{0}' must be one of the following types: {1}".format(varName,types))
# 		print("\n-----------------------------------------------------------")
# 		print("-----------------------------------------------------------\n")
#
# 		raise TypeError
#
# def value_check(var,values,checkType,varName="var"):
#
# 	if checkType in ["discrete","d"]:
# 		"""
# 		Discrete -- check whether to see if the 'var' is in the 'values' set
# 		"""
# 		if var not in values:
# 			print("-----------------------------------------------------------")
# 			print("-----------------------------------------------------------")
# 			print("                       VALUE ERROR                       \n")
# 			print("'{0}' must be one of the following values {1}".format(varName,values))
# 			print("\n-----------------------------------------------------------")
# 			print("-----------------------------------------------------------\n")
#
# 			raise ValueError
#
# 	elif checkType in ["forbidden","f"]:
# 		values = (values,) if ( (type(values) in [list,tuple]) == False ) else values
# 		"""
# 		Forbidden -- checks whether the 'var' is in the set of forbidden 'values'
# 		"""
# 		if var in values:
# 			print("-----------------------------------------------------------")
# 			print("-----------------------------------------------------------")
# 			print("                       VALUE ERROR                       \n")
# 			print("'{0}' must be cannot be one of the following values {1}".format(varName,values))
# 			print("\n                                                          ")
# 			print("\n-----------------------------------------------------------")
# 			print("-----------------------------------------------------------\n")
# 			raise ValueError
#
# 	elif checkType in ["boundary","b"]:
# 		"""
# 		Boundry -- checks whether the 'var' is in the range (value[0] , value[1])
# 		"""
# 		if values[0] == ":":
# 			if var > values[1]:
# 				print("-----------------------------------------------------------")
# 				print("-----------------------------------------------------------")
# 				print("                       VALUE ERROR                       \n")
# 				print("'{0}' must larger than {1}".format(varName,values[0]))
# 				print("\n                                                          ")
# 				print("\n-----------------------------------------------------------")
# 				print("-----------------------------------------------------------\n")
#
# 				raise ValueError
#
# 		elif values[1] == ":":
# 			if var < values[0]:
# 				print("-----------------------------------------------------------")
# 				print("                       VALUE ERROR                       \n")
# 				print("'{0}' must less than {1}".format(varName,values[1]))
# 				print("\n                                                          ")
# 				print("\n-----------------------------------------------------------\n")
# 				raise ValueError
# 		else:
# 			if var > values[1] or var < values[0]:
# 				print("-----------------------------------------------------------")
# 				print("-----------------------------------------------------------")
# 				print("                       VALUE ERROR                       \n")
# 				print("'{0}' must be in range {1}".format(varName,values))
# 				print("\n                                                          ")
# 				print("\n-----------------------------------------------------------")
# 				print("-----------------------------------------------------------\n")
# 				raise ValueError
#
# 	elif checkType in ["greater than","greater",">","g"]:
# 		"""
# 		Greater than -- checks to see if the 'var' is greater than 'values'
#
# 		raises ValueError if var less than values
# 		"""
# 		values = values[0] if type(values) in (tuple,list) else values
# 		if var < values:
# 			print("-----------------------------------------------------------")
# 			print("-----------------------------------------------------------")
# 			print("                       VALUE ERROR                       \n")
# 			print("'{0}' must be greater than {1}".format(varName,values))
# 			print("\n                                                          ")
# 			print("\n-----------------------------------------------------------")
# 			print("-----------------------------------------------------------\n")
#
# 			raise ValueError
#
# 	elif checkType in ["less than","less","<",'l']:
# 		values = values[0] if type(values) in (tuple,list) else values
# 		if var > values:
# 			print("-----------------------------------------------------------")
# 			print("-----------------------------------------------------------")
# 			print("                       VALUE ERROR                       \n")
# 			print("'{0}' must be less than {1}".format(varName,values))
# 			print("\n                                                          ")
# 			print("\n-----------------------------------------------------------")
# 			print("-----------------------------------------------------------\n")
#
# 			raise ValueError
#
#
# 	elif checkType in ["equals","e","="]:
# 		if var != values:
# 			print("-----------------------------------------------------------")
# 			print("-----------------------------------------------------------")
# 			print("                       VALUE ERROR                       \n")
# 			print("'{0}' must be equal to {1}".format(varName,values))
# 			print("\n                                                          ")
# 			print("\n-----------------------------------------------------------")
# 			print("-----------------------------------------------------------\n")
#
# 			raise ValueError
#
#
# if __name__ == "__main__":
#
#
# # #
# # # def path_check(path):
# # # 	if os.path.exists(path) == False:
# # # 		print("file path '{0}' does not exist".format(path))
# # # 		sys.exit()
# # # """
# # # ---------------------------------------------------------------------------------
# # #            UNABLE TO EFFECTIVELY CREATE CUSTOM ERRORS --> come back later
# # # ---------------------------------------------------------------------------------
# # """
#
# # def array_type_check(array1,array2,array1Name="array1",array2Name="array2"):
# # 	if array1.dtype != array2.dtype:
# # 		raise ArrayTypeError(array1,array2)
# # 		print("Is this working")
#
#
# # class ArrayTypeError(Exception):
# # 	"""
# # 	Raise in the event that two arrays are not of the same Type
#
# # 	This must be called after the arrays have already be validated to be numpy arrays
# # 	"""
# # 	def __init__(self,array1,array2,message="array types incompatible"):
# # 		self._a1Type = array1.dtype
# # 		self._a2Type = array2.dtype
# # 		self.message = message
# 		# super(ArrayTypeError,self).__init__(message,array1,array2)
#
#
# # class ArrayShapeError(Exception):
# # """
# # Raise in the event that two arrays are not the same size
#
# # This must be called after the arrays have already be validated to be numpy arrays
# # """
# # 	def __init__(self,message="array ",array1,array2):
# # 		self._array1Shape = array1.shape
# # 		self._array2Shape = array2.shape
# # 		self._message = "arrays sizes incompatible\r\n\r\narray1:{0}\r\narray2{2}".format(self._array1Shape,self._array2Shape)
#
# # 		super(ArrayShapeError,self).__init__(message,array1,array2)
#
#
#
# # if __name__ == "__main__":
# # 	import numpy as np
# # 	a = np.asarray( [1,2,3,4,5] )
# # 	b = np.asarray( [1.0,2.0,3.0,4.0,5.0] )
#
# # 	array_type_check(a,b)
