import numpy as np
from config import DELTA, SIGMA, get_pop_seed
from model.chromosome import Chromosome
from model.population import Population
from model.encoding import Encoder
from math import exp


class FitnessFunc:
    def __init__(self, chr_length: int):
        if chr_length < 0:
            raise ValueError("The chromosome length should be non-negative!")
        self.chr_length = chr_length
        self.optimal = None

    def apply(self, genotype):
        raise NotImplementedError()

    def get_optimal(self):
        raise NotImplementedError()
    
    def get_phenotype(self, genotype):
        raise NotImplementedError()

    def generate_population_for_run(self, run_i, n_optimal=1):
        return Population(self, seed=get_pop_seed(run_i), n_optimal=n_optimal)
    
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


class FH(FitnessFunc):
    def __init__(self, chr_length, encoder: Encoder):
        super().__init__(chr_length)
        self.encoder = encoder

    def apply(self, genotype):
        if len(genotype) != self.chr_length:
            raise ValueError("Incorrect length of genotype!")
        k = len([True for gene in genotype if gene == b'1'])
        return (self.chr_length - k)

    def get_optimal(self):
        if not self.optimal:
            self.optimal = Chromosome(0, np.full(self.chr_length, b'0'), self)
        return self.optimal

    def get_phenotype(self, genotype):
        if len(genotype) != self.chr_length:
            raise ValueError("Incorrect length of genotype!")
        return self.encoder.decode(genotype)


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
            self.optimal = Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)


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

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)


class Rastrigin(FitnessFunc):
    def __init__(self, a, encoder: Encoder):
        self.a = a
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = self.__apply(v)

    def __apply(self, genotype):
        x = self.encoder.decode(genotype)
        return np.abs(10 * np.cos(2 * np.pi * self.a) - self.a ** 2) \
                    + 10 * np.cos(2 * np.pi * x) - x**2

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return self.__apply(genotype)

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(0)
            self.optimal = Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)


class Deb2(FitnessFunc):
    def __init__(self, encoder: Encoder):
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = self.__apply(v)

    def __apply(self, genotype):
        x = self.encoder.decode(genotype)
        return np.exp(-2 * np.log(2) * ((x - 0.1) / 0.8) ** 2) * np.sin(5 * np.pi * x) ** 6

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return self.__apply(genotype)

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(0.1)
            self.optimal = Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)


class Deb4(FitnessFunc):
    def __init__(self, encoder: Encoder):
        super().__init__(encoder.length)
        self.encoder = encoder
        self.is_caching = encoder.length <= 12
        self.cache_dict = {}
        if self.is_caching:
            for v in self.encoder.get_all_values():
                self.cache_dict[v.tobytes()] = self.__apply(v)

    def __apply(self, genotype):
        x = self.encoder.decode(genotype)
        return np.exp(-2 * np.log(2) * ((x - 0.08) / 0.854) ** 2) * \
            np.sin(5 * np.pi * (x ** 0.75 - 0.05)) ** 6

    def apply(self, genotype):
        if self.is_caching:
            return self.cache_dict[genotype.tobytes()]
        return self.__apply(genotype)

    def get_optimal(self):
        if not self.optimal:
            optimal_genotype = self.encoder.encode(0.08)
            self.optimal = Chromosome(0, optimal_genotype, self)
        return self.optimal

    def get_phenotype(self, genotype):
        return self.encoder.decode(genotype)


if __name__ == "__main__":
    from model.encoding import *
    # fh = FH(7, BinaryEncoder(7))
    # genotype = np.array([b'0', b'0', b'0', b'1', b'0', b'0', b'1'])
    # print(fh.apply(genotype))
    # # print(fh.apply(b'0')) # raises ValueError
    # print(fh.get_optimal())
    # print(fh.get_phenotype(genotype))
    # # print(fh.get_phenotype(b'1')) # raises ValueError

    # print("---------------------------")
    # print("Rastrigin")
    # float_enc = FloatEncoder(-5.12, 5.11, 10)
    # x = 0
    # x_enc = float_enc.encode(x)
    # rastrigin = Rastrigin(7, float_enc)
    # print(f"f(0) = {rastrigin.apply(x_enc)}")
    # print(f"The optimal phenotype is: {rastrigin.get_phenotype(rastrigin.get_optimal().genotype)}")

    print("---------------------------")
    print("Decreasing maxima, Deb’s test function 2")
    float_enc = FloatEncoder(0, 1.023, 10)
    x = 0.1
    x_enc = float_enc.encode(x)
    deb2 = Deb2(float_enc)
    print(f"f(0.1) = {deb2.apply(x_enc)}")
    print(f"The optimal phenotype is: {deb2.get_phenotype(deb2.get_optimal().genotype)}")

    print("---------------------------")
    print("Uneven decreasing maxima, Deb’s test function 4")
    float_enc = FloatEncoder(0, 1.023, 10)
    x = 0.08
    x_enc = float_enc.encode(x)
    deb4 = Deb4(float_enc)
    print(f"f(0.08) = {deb4.apply(x_enc)}")
    print(f"The optimal phenotype is: {deb4.get_phenotype(deb4.get_optimal().genotype)}")
