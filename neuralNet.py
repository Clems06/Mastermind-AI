import numpy as np

class Net():
    def __init__(self, topology: list, activation: str, weigths_biases=[]):
        #Forme du réseau. ex: [2, 5, 3]  = 2 neurones d'entrée, une couche cachée de 5 neurones et 3 neurones de sortie
        self.topology = topology
        self.length = len(topology)

        """Liste des connections. i-eme position: connections entre couche i et i+1
        [ [1er neurone couche i -> 1er neurone couche i+1, 1er neurone couche i -> 2eme neurone couche i+1, ...]
          [2eme neurone couche i -> 1er neurone couche i+1, 2eme neurone couche i -> 2eme neurone couche i+1, ...]
          ...
        ]
        """
        if weigths_biases:
            self.weights = weigths_biases[0]
            self.biases = weigths_biases[1]
        else:
            self.weights = [np.random.rand(topology[i], topology[i+1]) for i in range(len(self.topology)-1)]
            #Biais des neurones. biases[i] -> i+1eme couche
            self.biases = [np.full(topology[i+1], 0) for i in range(len(self.topology)-1)]

        self.activation = activation
        self.activation_func = {"sigmoid":np.vectorize(self.sigmoid), "tanh":np.tanh}[activation]

    def __len__(self):
        return self.length

    def __copy__(self):
        return Net(self.topology, self.activation, [self.weights, self.biases])

    def sigmoid(self, x):
        return 1/(1+np.exp(-4*x))

    def getOutput(self, input: iter):
        values = np.array(input)
        for weights, biases in zip(self.weights, self.biases):
            #Effectuer le calcul d'une couche (utilisation des matrices pour simplifier l'écriture)
            print(values)
            values = self.activation_func(np.matmul(values, weights) + biases)
        return values

    def mutate(self, epsilon=0.1):
        # random boolean mask for which values will be changed
        for layer in self.weights:
            mask_random = np.random.choice([0, 1], size=layer.shape, p=((1 - epsilon), epsilon)).astype(np.bool)
            mask_completely_random = np.random.choice([0, 1], size=layer.shape, p=((1 - epsilon), epsilon)).astype(np.bool) * mask_random
            random_products = np.random.randn(*layer.shape)*0.5+1
            completely_random = np.random.rand(*layer.shape) * 10

            layer[mask_random] *= random_products[mask_random]
            layer[mask_completely_random] = completely_random[mask_completely_random]

    def combine(self, other):
        for i in range(len(self.weights)):
            layer1 = self.weights[i]
            layer2 = other.weights[i]

            mask_random = np.random.choice([0, 1], size=layer1.shape, p=(0.5, 0.5)).astype(np.bool)
            layer1[mask_random] = layer2[mask_random]








net = Net([2, 5, 3], "sigmoid")
print(net.getOutput([0, 0]))
print()

