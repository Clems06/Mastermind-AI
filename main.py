from LSTM import Population
from environment import *
import numpy as np
from github import Github

token="ghp"+"_kAPYTVnLUCao5zAupm0HTN3rucmPVL3i19vB"
g = Github(token)
database=g.get_repo("Clems06/Mastermind-AI")

class Main:
    def __init__(self):
        # 15 entrees: 3x4 (couleurs) + 2 (noir et blanc) + 1 (premier coup)
        # 12 sorties: 3x4 (couleurs)
        self.n_individual = 10
        self.population = Population((15, 12), self.n_individual)

    def save_current(self, gen, best_scores, average, openings):
        file = database.get_contents("database/general.csv", ref="database")
        content = file.decoded_content.decode().split('\n')
        openings = '|'.join([';'.join([''.join([str(i) for i in c]) for c in o]) for o in openings])
        content[1]=','.join(('c_'+str(gen),'|'.join(best_scores),str(average),openings))
        database.update_file(file.path, "dev", '\n'.join(content), file.sha, branch="database")

    def save_generation(self, gen, best_score, average, opening):
        file = database.get_contents("database/general.csv", ref="database")
        content = file.decoded_content.decode().split('\n')
        opening = ';'.join([''.join([str(i) for i in c]) for c in opening])
        content.append(','.join((str(gen), str(best_score),str(average),opening)))
        database.update_file(file.path, "dev", '\n'.join(content), file.sha, branch="database")

    def main_loop(self):
        num_generations = 100
        num_opening_moves = 3
        save_gen_every = 5

        self.population.first_generation()
        for generation in range(num_generations):
            print("Starting generation",generation)
            scores, openings = self.get_scores(self.population.population, self.population.keep_best, num_opening_moves) #[score, population]
            print(sorted(scores, key=lambda x: x[0])[-self.population.keep_best:])
            best = sorted(scores, key=lambda x: x[0])[-self.population.keep_best:]
            average = sum([-i[0]/100 for i in scores])/self.n_individual
            self.save_current(generation, [str(-i[0]/100) for i in best], average, openings)
            if generation%5==0:
                self.save_generation(generation, -best[-1][0]/100, average, openings[-1])
            self.population.new_generation(np.array([i[1] for i in best]))

    def get_scores(self, population:iter, n_openings:int, n_moves_per_opening:int):
        scores=[]
        openings=[]
        for individual, n in zip(population, range(len(population))):
            temp, opening = self.get_score(individual, opening=int(n<n_openings)*n_moves_per_opening)
            print("New individual", temp)
            scores.append((temp, individual))
            if n<n_openings:
                openings.append(opening)
        return scores, openings

    def get_score(self, individual, opening=0):
        num_games = 3
        tries_limit = 30
        first_game, opening=self.play_game(individual, tries_limit, opening=opening)
        games=[self.play_game(individual, tries_limit)[0] for _ in range(num_games-1)]+[first_game]
        return sum(games)/num_games, opening

    def play_game(self, individual, tries_limit:int, opening=0):
        board = Board()
        opening_moves=[]
        for coup in range(tries_limit):
            inputs = board.toinput()
            output = individual.get_output(inputs) / 2 + 0.5
            encoded_output = tuple([round(output[i])*4+round(output[i+1])*2+round(output[i+2])+1 for i in range(0, 10, 3)])
            if coup<opening:
                opening_moves.append(encoded_output)
            encoded_output = todict(encoded_output)
            if encoded_output == board.pwd:
                return -coup*100, opening_moves
            elif len(board.p) == 1:
                return -(coup+1) * 100, opening_moves

            board.append(encoded_output)


        return -len(board.p)-tries_limit*100, opening_moves


main=Main()
main.main_loop()