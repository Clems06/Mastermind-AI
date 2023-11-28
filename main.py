import csv
from environment import *
import numpy

class Main:

    def __init__(self, database_path:str):

        self.database=database_path

    def store_generation(self, generation:int, best, opening:iter):
        f_infos = []
        with open(self.database, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                f_infos.append(row)
        print(f_infos)
        gens=f_infos[0]
        bests=f_infos[1]
        openings=f_infos[2]
        gens.append(generation)
        bests.append(best)
        openings.append(opening)

        with open(self.database, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';',quoting=csv.QUOTE_MINIMAL)
            writer.writerow(gens)
            writer.writerow(bests)
            writer.writerow(openings)

    def get_score(self, population:iter, mode=numpy.sum):
        scores={}
        for individual in population:
            scores[individual]=mode(self.play_game(individual,tries_limit,True))
        return scores

    def play_game(self, individual, tries_limit:int, scores_only=False):
        pass

main=Main('test.csv')
main.get_score(1)