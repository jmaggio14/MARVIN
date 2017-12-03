# import numpy as np
# import marvin
#
#
# class SimpleNeuralNet(object):
#     def __init__(self,seed=0):
#         self.rng = marvin.RandomNumberGenerator(seed)
#         self.synaptic_weights = 2 * self.rng.random((3,1)) -1
#
#
#     def __sigmoid(self,x):
#         ret = 1.0 / (1.0 + np.exp(-x))
#         return ret
#
#     def __sigmoidDerivative(self,x):
#         ret = x * (1-x)
#
#     def predict(self,inputs):
#          sigmoid = self.__sigmoid(np.dot(inputs,weights))
#          return sigmoid
#
#      def train(self,training_set_inputs,training_set_outputs,num_iterations):
#          for i in range(num_iterations):
#              output = self.predict(training_set_inputs)
#              error = training_set_inputs - output
#              adjustment = np.dot(training_set_inputs.T,error*self.__sigmoidDerivative(output))
#              #adjusting the weights
#              self.synaptic_weights += adjustment
