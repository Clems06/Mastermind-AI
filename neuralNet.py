import numpy as np

class Net():
    def __init__(self, topology: list):
        #Forme du réseau. ex: [2, 5, 3]  = 2 neurones d'entrée, une couche cachée de 5 neurones et 3 neurones de sortie
        self.topology = topology
        self.length = len(topology)

        """Liste des connections. i-eme position: connections entre couche i et i+1
        [ [1er neurone couche i -> 1er neurone couche i+1, 1er neurone couche i -> 2eme neurone couche i+1, ...]
          [2eme neurone couche i -> 1er neurone couche i+1, 2eme neurone couche i -> 2eme neurone couche i+1, ...]
          ...
        ]
        """
        self.weights = [np.full((topology[i], topology[i+1]), 1) for i in range(len(self.topology)-1)]

        #Biais des neurones. biases[i] -> i+1eme couche
        self.biases = [np.full(topology[i+1], 0) for i in range(len(self.topology)-1)]

        self.vec_sigmoid = np.vectorize(self.sigmoid)

    def __len__(self):
        return self.length

    def sigmoid(self, x):
        return 1/(1+np.exp(-4*x))

    def getOutput(self, input: iter):
        values = np.array(input)
        for weights, biases in zip(self.weights, self.biases):
            #Effectuer le calcul d'une couche (utilisation des matrices pour simplifier l'écriture)
            print(values)
            values = self.vec_sigmoid(np.matmul(values, weights) + biases)
        return values



net = Net([2, 5, 3])
print(net.getOutput([0, 0]))
print()

