import time
from random import choices, random

from . import BasicModel

class RandomModel(BasicModel):

    def __init__(self, name="test", options=[BasicModel.jump,BasicModel.duck, BasicModel.none], weights=None):
        super().__init__(name)
        self.options = options
        self.weights = weights if weights is not None else [random() for i in range(len(self.options))]
        
    def act(self):
        action = choices(self.options, weights=self.weights)[0]
        action()
