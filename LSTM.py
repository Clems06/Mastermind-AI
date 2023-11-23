from neuralNet import *
class LSTM():
    def __init__(self, input_size, output_size):
        self.forget_gate = Net([input_size+output_size, 5, 5, output_size])
        self.input_gate = Net([input_size+output_size, 5, 5, output_size])