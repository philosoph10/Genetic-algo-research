import numpy as np
from config import N, EPS, N_LAST_GENS
from model.chromosome import Chromosome
from copy import deepcopy, copy


class Population:
    def __init__(self, fitness_function, seed=0, chromosomes=None):
        self.fitness_function = fitness_function

        if chromosomes is not None:
            self.chromosomes = chromosomes
        else:
            self.chromosomes = np.empty(N, dtype=object)
            self.chromosomes[0] = copy(fitness_function.get_optimal())
            rng = np.random.default_rng(seed=seed)
            for chr_i in range(1, N):
                genotype = rng.choice([b'0', b'1'], fitness_function.chr_length)
                self.chromosomes[chr_i] = Chromosome(chr_i, genotype, fitness_function)

        self.update()

    def has_converged(self, f_avgs, param_names):
        has_mutation = 'mut' in param_names[2]

        if not has_mutation:
            return self.is_homogenous_100()
            
        if param_names[0] == 'FconstALL':
            return self.is_homogenous_99()

        return self.has_f_avg_converged(f_avgs)
    
    def has_f_avg_converged(self, f_avgs):
        if len(f_avgs) < N_LAST_GENS:
            return False

        diffs = []
        for i in range(1, len(f_avgs)):
            curr = f_avgs[i]
            prev = f_avgs[i-1]
            diffs.append(abs(curr - prev))

        return all(x <= EPS for x in diffs)
    
    def is_homogenous_99(self):
        l = self.fitness_function.chr_length
        for i in range(l):
            n_zeros = len([True for g in self.genotypes if g[i] == b'0'])
            percentage = n_zeros / N
            if percentage > 0.01 and percentage < 0.99:
                return False
        return True

    def is_homogenous_100(self):
            return all([np.array_equal(geno, self.genotypes[0]) for geno in self.genotypes[1:]])

    def found_close_to_optimal(self):
        for chr in self.chromosomes:
            if self.fitness_function.check_chromosome_success(chr):
                return True
        return False

    def get_fitness_max(self):
        res = np.max(self.fitnesses)
        return res

    def get_fitness_avg(self):
        return np.mean(self.fitnesses)

    def get_fitness_std(self):
        return np.std(self.fitnesses)
    
    def count_fitness_at_least(self, min_fitness):
        return len([True for f in self.fitnesses if f >= min_fitness])

    def count_optimal_genotype(self):
        optimal = self.fitness_function.get_optimal().genotype
        return len([True for g in self.genotypes if np.array_equal(g, optimal)])

    def get_ids(self):
        return [chr.id for chr in self.chromosomes]

    def update(self):
        self.fitnesses = np.array([chr.fitness for chr in self.chromosomes])
        self.genotypes = np.array([chr.genotype for chr in self.chromosomes])

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()
    
    def __deepcopy__(self, memo):
        return Population(self.fitness_function, chromosomes=deepcopy(self.chromosomes))
    
    def __str__(self):
        return str(np.array([str(chr) for chr in self.chromosomes]))