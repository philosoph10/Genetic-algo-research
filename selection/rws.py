from config import G, N
import numpy as np
from selection.selection_method import SelectionMethod
from copy import copy


class RWS(SelectionMethod):
    def select(self, population):
        fitness_list = population.fitnesses
        fitness_sum = sum(fitness_list)

        if fitness_sum == 0:
            fitness_list = [0.0001 for _ in fitness_list]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in fitness_list]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)


class DisruptiveRWS(SelectionMethod):
    def select(self, population):
        f_avg = population.get_fitness_avg()
        f_scaled = [abs(fitness - f_avg) for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)


class BlendedRWS(SelectionMethod):
    def __init__(self):
        self.i = 0

    def select(self, population):
        f_scaled = [fitness / (G + 1 - self.i) for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

        self.i += 1


class WindowRWS(SelectionMethod):
    def __init__(self, h=2):
        self.h = h
        self.f_h_worst = []

    def select(self, population):
        if len(self.f_h_worst) < self.h:
            self.f_h_worst.append(min(population.fitnesses))
        else:
            self.f_h_worst[0] = self.f_h_worst[1]
            self.f_h_worst[1] = min(population.fitnesses)
        f_worst = min(self.f_h_worst)

        f_scaled = [fitness - f_worst for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)
