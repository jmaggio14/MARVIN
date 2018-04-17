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
import time

def retry_on_fail(target,
                    args=[],
                    kwargs={},
                    retries=5,
                    wait_time=5e-3,
                    exceptions=None):
    """
        a method which reruns a target function a set number of retries
        or until the target function runs without error

        input::
            target (func):
                    the target function pointer
            args (list) = []:
                    a list of arguments to be unpacked for the
                    target function
            kwargs (dict) = {}:
                    keyword arguments to be unpacked for the
                    target function
            retries (int,float) = 5:
                    the number of times to retry the target function
            wait_time (float) = 5e-3:
                    the time in seconds to wait in between retries
            exceptions (iterable,Exception) = None:
                    Exception or list of Exceptions that demand a retry.
                    leaving it None will result in any exception
                    demanding a retry

        return::
            ret (any type):
                the return value of the target function if it succeeded,
                or None if the function continously throws an error
    """
    assert callable(target),"'target' must be callable"
    assert isinstance(args,(list,tuple)),"'args' must be a list or tuple"
    assert isinstance(kwargs,dict),"'kwargs' must be a dict"
    assert isinstance(retries,int),"'retries must be an int'"
    assert isinstance(wait_time,(int,float)),"'wait_time' must be a number"
    assert isinstance(exceptions,(type(None),list,tuple)),\
                                "'exceptions must be list,tuple or NoneType"

    if exceptions == None:
        exceptions = Exception

    for i in range(retries):
        try:
            ret = target(*args,**kwargs)
            return ret

        except exceptions:
            time.sleep(wait_time)
            continue

        except Exception:
            break
