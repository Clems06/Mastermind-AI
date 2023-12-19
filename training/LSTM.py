import numpy as np
import copy
import random

def sigmoid(x):
    return 1 / (1 + np.exp(-4 * x))

vec_sigmoid = np.vectorize(sigmoid)

def mutate_list(layer, epsilon=0.1, alpha=0.1):
    mask_random = np.random.choice([0, 1], size=layer.shape, p=((1 - epsilon), epsilon)).astype(bool)
    mask_completely_random = np.random.choice([0, 1], size=layer.shape, p=((1 - alpha), alpha)).astype(bool) * mask_random
    random_products = np.random.randn(*layer.shape) * 0.5 + 1
    completely_random = np.random.rand(*layer.shape) * 10

    layer[mask_random] *= random_products[mask_random]
    layer[mask_completely_random] = completely_random[mask_completely_random]

def combine_lists(list1, list2):
    mask_random = np.random.choice([0, 1], size=list1.shape, p=(0.5, 0.5)).astype(bool)
    list1[mask_random] = list2[mask_random]

class Gate:
    def __init__(self, input_size, output_size, activation_function, model=[]):
        self.input_size = input_size
        self.output_size = output_size

        if model:
            self.gate_input, self.gate_recurrent, self.gate_bias = model
        else:
            self.gate_input = np.random.rand(input_size, output_size) * 2 - 1
            self.gate_recurrent = np.random.rand(output_size, output_size) * 2 - 1
            self.gate_bias = np.random.rand(output_size) * 2 - 1

        self.activation_name = activation_function
        self.activation = {"sigmoid": vec_sigmoid, "tanh":np.tanh}[activation_function]

    def __copy__(self):
        return Gate(self.input_size, self.output_size, self.activation_name, [np.copy(self.gate_input), np.copy(self.gate_recurrent), np.copy(self.gate_bias)])

    def gate_output(self, input_list, prev_output):
        return self.activation(input_list.dot(self.gate_input) + prev_output.dot(self.gate_recurrent) + self.gate_bias)

    def mutate(self, epsilon=0.1, alpha=0.1):
        mutate_list(self.gate_input, epsilon, alpha)
        mutate_list(self.gate_recurrent, epsilon, alpha)
        mutate_list(self.gate_bias, epsilon, alpha)

    def combine(self, other):
        combine_lists(self.gate_input, other.gate_input)
        combine_lists(self.gate_recurrent, other.gate_recurrent)
        combine_lists(self.gate_bias, other.gate_bias)


class LSTM:
    def __init__(self, input_size, output_size, gates=[]):
        self.input_size = input_size
        self.output_size = output_size

        if gates:
            self.forget_gate, self.input_gate, self.output_gate, self.memory_gate = gates
        else:
            self.forget_gate = Gate(input_size, output_size, "sigmoid")
            self.input_gate = Gate(input_size, output_size, "sigmoid")
            self.output_gate = Gate(input_size, output_size, "sigmoid")
            self.memory_gate = Gate(input_size, output_size, "tanh")

    def __copy__(self):
        return LSTM(self.input_size, self.output_size, [copy.copy(self.forget_gate), copy.copy(self.input_gate), copy.copy(self.output_gate), copy.copy(self.memory_gate)])

    def recurrent_step(self, input_list, prev_output, memory_cell):
        forget_gate = self.forget_gate.gate_output(input_list, prev_output)
        input_gate = self.input_gate.gate_output(input_list, prev_output)
        output_gate = self.output_gate.gate_output(input_list, prev_output)
        retain_gate = self.memory_gate.gate_output(input_list, prev_output)

        new_memory = memory_cell*forget_gate + input_gate*retain_gate
        output = output_gate * np.tanh(new_memory)

        return output, new_memory

    def get_output(self, inputs):
        cell_memory = np.zeros(self.output_size)
        output = np.zeros(self.output_size)
        for input in inputs:
            output, cell_memory = self.recurrent_step(input, output, cell_memory)

        return output

    def mutate(self, epsilon=0.1, alpha=0.1):
        self.forget_gate.mutate(epsilon, alpha)
        self.input_gate.mutate(epsilon, alpha)
        self.output_gate.mutate(epsilon, alpha)
        self.memory_gate.mutate(epsilon, alpha)

    def combine(self, other):
        self.forget_gate.combine(other.forget_gate)
        self.input_gate.combine(other.input_gate)
        self.output_gate.combine(other.output_gate)
        self.memory_gate.combine(other.memory_gate)

class Population:
    def __init__(self, sizes, population_size):
        self.population_size = population_size
        self.input_size, self.output_size = sizes

        self.population = []
        self.keep_best = population_size//10

    """def main_loop(self):
        num_generations = 100

        self.population = np.array([LSTM(self.input_size, self.output_size) for _ in range(self.population_size)])
        for generation in range(num_generations):
            print("Starting generation",generation)
            scores = self.environment.get_score(self.population, generation) #[score, population]
            best = np.array([i[1] for i in np.sort(scores)[:self.keep_best]])
            self.population = self.new_generation(best)"""

    def first_generation(self):
        self.population = np.array([LSTM(self.input_size, self.output_size) for _ in range(self.population_size)])

    def new_generation(self, best):
        self.population = best

        gamma = 0.1
        epsilon = 0.1
        alpha = 0.1

        for i in range(self.population_size - len(best)):
            choice = copy.copy(np.random.choice(best, 1)[0])
            choice.mutate(epsilon, alpha)
            if random.random() < gamma:
                choice2 = copy.copy(np.random.choice(best, 1)[0])
                choice.combine(choice2)

            self.population = np.append(self.population, choice)




