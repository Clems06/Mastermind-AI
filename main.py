import csv
from LSTM import Population
from environment import *
import numpy as np

class Main:
    def __init__(self):
        # 15 entrees: 3x4 (couleurs) + 2 (noir et blanc) + 1 (premier coup)
        # 12 sorties: 3x4 (couleurs)
        self.population = Population((15, 12), 100)


    def main_loop(self):
        num_generations = 100

        self.population.first_generation()
        for generation in range(num_generations):
            print("Starting generation",generation)
            scores = self.get_scores(self.population.population) #[score, population]
            print(sorted(scores, key=lambda x: x[0])[-self.population.keep_best:])
            best = np.array([i[1] for i in sorted(scores, key=lambda x: x[0])[-self.population.keep_best:]])
            self.population.new_generation(best)

    def get_scores(self, population:iter):
        scores=[]
        for individual in population:

            temp = self.get_score(individual)
            print("New individual", temp)
            scores.append((temp, individual))
        return scores

    def get_score(self, individual):
        num_games = 10
        tries_limit = 30
        return sum([self.play_game(individual, tries_limit) for _ in range(num_games)])/num_games

    def play_game(self, individual, tries_limit:int):
        board = Board()
        for coup in range(tries_limit):
            inputs = board.toinput()
            output = individual.get_output(inputs) / 2 + 0.5
            encoded_output = tuple([round(output[i])*4+round(output[i+1])*2+round(output[i+2])+1 for i in range(0, 10, 3)])
            encoded_output = todict(encoded_output)

            if encoded_output == board.pwd:
                return -coup*100
            elif len(board.p) == 1:
                return -(coup+1) * 100

            board.append(encoded_output)


        return -len(board.p)-tries_limit*100


main=Main()
main.main_loop()