import numpy as np
import marvin
# # from numpy.random import RandomState
#
#
class RandomNumberGenerator(np.random.RandomState):
    """
    inherits from numpy.random.RandomState
    https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.random.RandomState.html

    wrapper class for numpy.random.RandomState --> provides an easy
    way to access an RNG with a specified seed and prevents possible
    rng collisions compared to programming which by default uses
    np.random(seed) as it's RNG.

    """
    def __init__(self,seed=None):
        super(RandomNumberGenerator,self).__init__(seed)
#
#
if __name__ == "__main__":
#     pass
    marvin.tests.test_RandomNumberGenerator()
