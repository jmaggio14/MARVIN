import time



def retryOnFail(target,args=[],kwargs={},retries=5,wait_time=5e-3,exceptions=None):
    """
        a method which reruns a target function a set number of retries or until
        the target function runs without error

        input::
            target (function pointer): the target function pointer
            args (iterable): a list of arguments to be unpacked for the target function
            kwargs (dict): keyword arguments to be unpacked for the target function
            retries (int): the number of times to retry the target function
            wait_time (float): the time in seconds to wait in between retries
            exceptions (iterable,Exception): Exception or list of Exceptions that demand
                a retry. leaving it None will result in any exception demanding a retry

        return::
            ret (any type): the return value of the target function if it succeeded,
                or None if the function continously throws an error
    """
    if exceptions == None:
        exceptions = Exception

    for i in range(retries):
        try:
            ret = target(*args,**kwargs)
            return ret
        except exceptions:
            time.sleep(wait_time)
            continue
