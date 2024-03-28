from config import G, N
import numpy as np
from model.population import Population
from selection.selection_method import SelectionMethod
from copy import copy


class FUSS(SelectionMethod):

    def __init__(self):
        self.f_min = None
        self.f_max = None

    def select(self, population):
        fitness_max = population.get_fitness_max()
        fitness_min = population.get_fitness_min()

        if self.f_min is None or self.f_min > fitness_min:
            self.f_min = fitness_min
        if self.f_max is None or self.f_max < fitness_max:
            self.f_max = fitness_max
        
        chosen = []
        for i in range(N):
            x = np.random.uniform(self.f_min, self.f_max)
            ind = self.__find_closest(population.fitnesses, x)
            chosen.append(population.chromosomes[ind])

        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

    @staticmethod
    def __find_closest(arr, x):
        """
        Findest the closest value to x in array arr.
        In case of ties, pick a random one
        """
        # Calculate absolute difference between each element and x
        diffs = np.abs(arr - x)
        
        # Find the minimum difference
        min_diff = np.min(diffs)
        
        # Create a boolean mask for elements with minimum difference
        mask = diffs == min_diff
        
        # Get the indices of the True values in the mask
        closest_indices = np.flatnonzero(mask)
        
        # Randomly choose one of the indices
        chosen_index = np.random.choice(closest_indices)
        
        # Return the corresponding element from arr
        return chosen_index