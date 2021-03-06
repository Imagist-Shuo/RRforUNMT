"""
Model Interface
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class NMTModel(object):
    """ Abstract object representing an NMT model """

    def __init__(self, params, scope):
        self._scope = scope
        self._params = params

    def get_training_func(self, initializer):
        """
        :param initializer: the initializer used to initialize the model
        :return: a function with the following signature:
            (features, params, reuse) -> loss
        """
        raise NotImplementedError("Not implemented")

    def get_evaluation_func(self):
        """
        :return: a function with the following signature:
            (features, params) -> score
        """
        raise NotImplementedError("Not implemented")

    def get_inference_func(self):
        """
        :returns:
            this function should returns a tuple of (encoding_fn, decoding_fn), 
            with the following requirements:
                encoding_fn: (features, params) -> initial_state
                decoding_fn: (feature, state, params) -> log_prob, next_state
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def get_name():
        raise NotImplementedError("Not implemented")

    @staticmethod
    def get_parameters():
        raise NotImplementedError("Not implemented")

    @property
    def parameters(self):
        return self._params
