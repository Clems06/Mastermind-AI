import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-4 * x))

vec_sigmoid = np.vectorize(sigmoid)

class LSTM():
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size

        self.forget_input = np.random.rand(input_size, output_size)
        self.forget_recurrent = np.random.rand(output_size, output_size)
        self.forget_bias = np.random.rand(output_size)

        self.input_input = np.random.rand(input_size, output_size)
        self.input_recurrent = np.random.rand(output_size, output_size)
        self.input_bias = np.random.rand(output_size)

        self.output_input = np.random.rand(input_size, output_size)
        self.output_recurrent = np.random.rand(output_size, output_size)
        self.output_bias = np.random.rand(output_size)

        self.memory_input = np.random.rand(input_size, output_size)
        self.memory_recurrent = np.random.rand(output_size, output_size)
        self.memory_bias = np.random.rand(output_size)

    def recurrent_step(self, input, prev_output, memory_cell):
        forget_gate = vec_sigmoid(input*self.forget_input + prev_output*self.forget_recurrent + self.forget_bias)
        input_gate = vec_sigmoid(input*self.input_input + prev_output*self.input_recurrent + self.input_bias)
        output_gate = vec_sigmoid(input*self.input_input + prev_output*self.input_recurrent + self.input_bias)
        retain_gate = np.tanh(input*self.input_input + prev_output*self.input_recurrent + self.input_bias)

        new_memory = memory_cell*forget_gate + input_gate*retain_gate
        output = output_gate * np.tanh(new_memory)

        return output, new_memory

    def getOutput(self, inputs):
        cell_memory = np.zeros(self.output_size)
        output = np.zeros(self.output_size)
        for input in inputs:
            output, cell_memory = self.recurrent_step(input, output, cell_memory)

        return output

    def mutate(self):
