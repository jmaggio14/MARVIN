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

class Payload(object):
    """Base Class for all Marvin Payload objects. This object is meant
    to be inherited from and overwritten by child Payload object which
    then define the functionality for their unique hardware

    functions:
        --------- (with NO default functionality) ---------
        retrieve(*args,**kwargs) --> retrieve data from the payload
        change_setting(*args,**kwargs) --> modifies payload behavior
        get_status(*args,**kwargs) --> gets payload status
        capture(*args,**kwargs) --> tells the payload to capture data
        close() --> closes the payload
        open() --> opens/reopens the payload

        ---------- (with default functionality) ----------
        get_payload_name() --> returns the name of the payload
        run_user_func(func_name,*args,**kwargs)--> runs another function
                                        in the (child) class

        ------------------- (operators) -------------------
        __repr__() --> calls __str__()
        __str__() --> returns object description as string
        __enter__() --> for with statement functionality, does nothing
        __exit__() --> runs the close function, does no error handling
        __getitem__() --> wrapper for retrieve()

    attributes::
        payload_name (string): the name of the payload

    """
    def __init__(self,payload_name):
        assert isinstance(payload_name,str), \
                                    "payload_name must be a string"
        self.payload_name = payload_name


    def retrieve(self,*args,**kwargs):
        """prototype meant to be overwritten to retrieve data from the
        payload

        Args:
            *args (undefined): defined in overwritten function
            **kwargs (undefined): defined in overwritten function

        Returns:
            ret (undefined): defined in overwritten function
        """
        pass

    def change_setting(self,args,**kwargs):
        """prototype meant to be overwritten to change a settings on the
        payload instrument

        Args:
            *args (undefined): defined in overwritten function
            **kwargs (undefined): defined in overwritten function

        Returns:
            ret (undefined): defined in overwritten function
        """
        pass

    def get_status(self,*args,**kwargs):
        """prototype meant to be overwritten to retrieve metadata about
        the instrument in question

        Args:
            *args (undefined): defined in overwritten function
            **kwargs (undefined): defined in overwritten function

        Returns:
            ret (undefined): defined in overwritten function
        """
        pass


    def capture(self,*args,**kwargs):
        """prototype meant to be overwritten used to tell the payload to
        capture data

        Args:
            *args (undefined): defined in overwritten function
            **kwargs (undefined): defined in overwritten function

        Returns:
            ret (undefined): defined in overwritten function
        """
        pass

    def close(self):
        """function meant to be overwritten, used to close the payload
        object

        Args:
        None
        Returns:
        ret (undefined): defined in overwritten function
        """
        pass

    def open(self):
        """function meant to be overwritten to open/reopen the payload
        Args:
            None
        Returns:
            None
        """
        pass


    def get_payload_name(self):
        """returns the name of the payload instance

        Args:
            None
        Returns:
            payload_name: the name of the payload instance
        """
        return self.payload_name



    def run_user_func(self,func_name,*args,**kwargs):
        """runs a user defined function that may not normally be
        accessible other Marvin's Flask system

        Args:
            func_name (string): the name of the function to be called,
                this function should be accessible as self.func
            *args (unpacked list): unpacked args for the user_func
            **kwargs (unpacked dict): unpacked kwargs for the user_func


        Returns:
            out (any type): the output from your user_func
        """
        # checking to see if the user_func exists and is callable
        assert isinstance(func_name,str),"func_name must be a string"


        if hasattr(self,func_name):
            user_func = getattr(self,func_name)
            if callable( user_func ):
                out = user_func(*args,**kwargs)
                return out
            else:
                raise TypeError("user_func is not callable")
        else:
            raise marvin.PayloadUserFuncNotFound(
                                "user_func '%s' not found in Payload '%s'"
                                % func_name,self.payload_name)



    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out_str = "Marvin Payload Object -- '{payload_name}'"\
                                .format(payload_name=self.payload_name)
        return out_str

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback_obj):
        """auto function closer for use with python 'with' statements
        calls the close function
        Does NOT do any exception handling
        """
        self.close()

    def __getitem__(self,key):
        return self.retrieve( key )
    # @classmethod
    # def __check_payload_name_validity(cls,payload_name):
    #     """checks and updates a class variable to determine whether or
    #     not the payload_name already exists as a instance of this
    #     class's child. if the name doesn't it exist, it will update
    #     the class variable so that all other instances know.
    #
    #     Note:
    #         may have to be updated to reference a global Queue to be
    #         made threadsafe
    #
    #     Arg:
    #         payload_name (str): the name of the payload
    #     Returns:
    #         name_is_valid (bool): whether or not the payload name is
    #         valid (ie doesn't already exist)
    #     """
    #     if hasattr(cls,"all_payload_names"):
    #         # payload_name already exists -- therefore is invalid
    #         if payload_name in cls.all_payload_names:
    #             return False
    #         #payload_name doesn't already exist and is valid
    #         else:
    #             cls.all_payload_names.append(payload_name)
    #             return True
    #     else:
    #         #payload_name doesn't exist because this is first instance
    #         cls.all_payload_names = [payload_name]
    #         return True
    #
# END
