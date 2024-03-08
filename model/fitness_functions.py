import numpy as np
from config import DELTA, SIGMA, get_pop_seed
from model.chromosome import Chromosome
from model.population import Population
from model.encoding import Encoder
from math import exp


class FitnessFunc:
    def __init__(self, chr_length):
        self.chr_length = chr_length
        self.optimal = None

    def apply(self, genotype):
        raise NotImplementedError()

    def get_optimal(self):
        raise NotImplementedError()
    
    def get_phenotype(self, genotype):
        raise NotImplementedError()

    def generate_population_for_run(self, run_i):
        return Population(self, seed=get_pop_seed(run_i))
    
    def check_chromosome_success(self, chr: Chromosome):
        y_diff = abs(chr.fitness - self.get_optimal().fitness)
        x_diff = abs(self.get_phenotype(chr.genotype) - self.get_phenotype(self.get_optimal().genotype))
        return y_diff <= DELTA and x_diff <= SIGMA


class FconstALL(FitnessFunc):
    def apply(self, genotype):
        return 100

    def get_optimal(self):
        if not self.optimal:
            self.optimal = Chromosome(0, np.full(self.chr_length, b'0'), self)
        return self.optimal
    
    def get_phenotype(self, genotype):
        return 0
    
    def check_chromosome_success(self, ch):
        return True


class FHD(FitnessFunc):
    def __init__(self, delta, chr_length):
        super().__init__(chr_length)
        self.delta = delta

    def apply(self, genotype):
        k = len([True for gene in genotype if gene == b'0'])
        return (self.chr_length - k) + k * self.delta

    def get_optimal(self):
        if not self.optimal:
            self.optimal = Chromosome(0, np.full(self.chr_length, b'0'), self)
        return self.optimal

    def get_phenotype(self, genotype):
        return len([True for gene in genotype if gene == b'1'])


class Fx2(FitnessFunc):
    def __init__(self, encoder: Encoder):
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = self.encoder.decode(v)**2

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return self.encoder.decode(genotype)**2

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(self.encoder.upper_bound)
            self.optimal =  Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, chromosome):
        return self.encoder.decode(chromosome)


class F5122subx2(FitnessFunc):
    def __init__(self, encoder: Encoder):
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = 5.12**2 - self.encoder.decode(v)**2

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return 5.12**2 - self.encoder.decode(genotype)**2

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(0)
            self.optimal =  Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)
    
class Fexp(FitnessFunc):
    def __init__(self, c, encoder: Encoder):
        self.c = c
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = exp(self.c * self.encoder.decode(v))

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return exp(self.c * self.encoder.decode(genotype))

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(self.encoder.upper_bound)
            self.optimal =  Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, chromosome):
        return self.encoder.decode(chromosome)