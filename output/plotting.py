import matplotlib.pyplot as plt
from config import N, OUTPUT_FOLDER
import os
from model.population import Population
from stats.generation_stats import GenerationStats
import numpy as np


def plot_run_stats(
        gen_stats_list: list[GenerationStats],
        param_names: tuple[str],
        run_i):
    reproduction_rates = [gen_stats.reproduction_rate for gen_stats in gen_stats_list if gen_stats.reproduction_rate is not None]
    losses_of_diversity = [gen_stats.loss_of_diversity for gen_stats in gen_stats_list if gen_stats.loss_of_diversity is not None]
    __plot_stat2(reproduction_rates, losses_of_diversity, param_names, run_i, 'Reproduction Rate', 'Loss of Diversity', 'rr_and_lod', y_lim=(0,1))

    if param_names[0] != 'FconstALL':
        f_avgs = [gen_stats.f_avg for gen_stats in gen_stats_list]
        __plot_stat(f_avgs, param_names, run_i, 'Fitness Average', 'f_avg')

        f_bests = [gen_stats.f_best for gen_stats in gen_stats_list]
        __plot_stat(f_bests, param_names, run_i, 'Highest Fitness', 'f_best')

        intensities = [gen_stats.intensity for gen_stats in gen_stats_list if gen_stats.intensity is not None]
        __plot_stat(intensities, param_names, run_i, 'Selection Intensity', 'intensity')

        differences = [gen_stats.difference for gen_stats in gen_stats_list if gen_stats.difference is not None]
        __plot_stat(differences, param_names, run_i, 'Selection Difference', 'difference')

        __plot_stat2(differences, intensities, param_names, run_i, 'Difference', 'Intensity', 'intensity_and_difference')

        f_stds = [gen_stats.f_std for gen_stats in gen_stats_list]
        __plot_stat(f_stds, param_names, run_i, 'Fitness Standard Deviation', 'f_std')

        optimal_counts = [gen_stats.optimal_count for gen_stats in gen_stats_list]
        __plot_stat(optimal_counts, param_names, run_i, 'Number of Optimal Chromosomes', 'optimal_count')

        growth_rates = [gen_stats.growth_rate for gen_stats in gen_stats_list]
        if len(growth_rates) > 0:
            growth_rates = growth_rates[1:]
        __plot_stat(growth_rates, param_names, run_i, 'Growth Rate', 'growth_rate')

        pr_fets = [gen_stats.P_FET for gen_stats in gen_stats_list]
        __plot_stat(pr_fets, param_names, run_i, 'Fisher Exact Pressure', 'fisher_exact', y_lim=None)

        pressures = [gen_stats.pr for gen_stats in gen_stats_list]
        __plot_stat(pressures, param_names, run_i, 'Selection Pressure', 'selection_pressure')

        kendall_taus = [gen_stats.Kendall_tau for gen_stats in gen_stats_list]
        __plot_stat(kendall_taus, param_names, run_i, 'Kendall Tau-b Pressure Test', 'kendall_tau', y_lim=(-1.01,1.01))

        fraction_of_best = [gen_stats.num_of_best / N for gen_stats in gen_stats_list]
        __plot_stat(fraction_of_best, param_names, run_i, 'Fraction of best individual accross generation', 'fraction_of_best', y_lim=(-0.01,1.01))

        # ns_unique = [gen_stats.n_unique for gen_stats in gen_stats_list]
        ns_unique = [gen_stats_list[0].n_unique_before_selection] + \
        [gen_stats.n_unique_after_selection for gen_stats in gen_stats_list]
        __plot_stat(ns_unique, param_names, run_i, '#unique chromosomes', 'n_unique')
                    

def plot_generation_stats(
        population: Population,
        param_names: tuple[str],
        run_i, gen_i, homogeneous_frac=None):
    __plot_genotype_distribution(population, param_names, run_i, gen_i, homogeneous_frac=homogeneous_frac)
    if param_names[0] != 'FconstALL':
        __plot_fitness_distribution(population, param_names, run_i, gen_i, homogeneous_frac=homogeneous_frac)
    if param_names[0] not in ['FconstALL', 'FHD', 'FH']:
        __plot_phenotype_distribution(population, param_names, run_i, gen_i, homogeneous_frac=homogeneous_frac)


def __plot_stat(
        data,
        param_names: tuple[str],
        run_i,
        ylabel,
        file_name,
        y_lim=None):
    param_hierarchy = __get_path_hierarchy(param_names, run_i)
    path = '/'.join(param_hierarchy)

    if not os.path.exists(path):
        os.makedirs(path)

    plt.plot(data)
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    x_size = len(data) if data[-1] is not None else len(data) - 1
    plt.xticks(range(x_size))
    if y_lim is not None:
        plt.ylim(*y_lim)
    plt.savefig(f'{path}/{file_name}.png')
    plt.close()

def __plot_stat2(
        data1, data2,
        param_names: tuple[str],
        run_i,
        label1, label2,
        file_name,
        y_lim=None):
    param_hierarchy = __get_path_hierarchy(param_names, run_i)
    path = '/'.join(param_hierarchy)

    if not os.path.exists(path):
        os.makedirs(path)

    plt.plot(data1, label=label1)
    plt.plot(data2, label=label2)

    if y_lim is not None:
        plt.ylim(*y_lim)

    plt.xlabel('Generation')
    plt.legend()
    plt.savefig(f'{path}/{file_name}.png')
    plt.close()

def __plot_fitness_distribution(
        population: Population,
        param_names: tuple[str],
        run_i, gen_i, homogeneous_frac=None):
    param_hierarchy = __get_path_hierarchy(param_names, run_i) + ['fitness']
    path = '/'.join(param_hierarchy)

    if homogeneous_frac is not None:
        path = os.path.join(path, 'homogeneous')

    if not os.path.exists(path):
        os.makedirs(path)

    x_max = population.fitness_function.get_optimal().fitness
    x_step = x_max / 100
    (x, y) = __get_distribution(population.fitnesses, x_max=x_max, x_step=x_step)
    plt.bar(x, y, width=x_step*0.8)
    plt.xlabel('Chromosome fitness')
    plt.ylabel('Number of chromosomes')
    save_file = f'{path}/{int(homogeneous_frac*100)}_{gen_i}.png' if homogeneous_frac is not None\
                else f'{path}/{gen_i}.png'
    plt.savefig(save_file)
    plt.close()

def __plot_phenotype_distribution(
        population: Population,
        param_names: tuple[str],
        run_i, gen_i, homogeneous_frac=None):
    
    param_hierarchy = __get_path_hierarchy(param_names, run_i) + ['phenotype']
    path = '/'.join(param_hierarchy)

    if homogeneous_frac is not None:
        path = os.path.join(path, 'homogeneous')

    if not os.path.exists(path):
        os.makedirs(path)

    phenotypes = [population.fitness_function.get_phenotype(geno) for geno in population.genotypes]
    encoder = population.fitness_function.encoder
    x_min = encoder.lower_bound
    x_max = encoder.upper_bound
    x_step = (x_max - x_min) / 100
    (x, y) = __get_distribution(phenotypes, x_min=x_min, x_max=x_max, x_step=x_step)
    plt.bar(x, y, width=x_step*0.8)
    plt.xlabel('Chromosome phenotype')
    plt.ylabel('Number of chromosomes')
    save_file = f'{path}/{int(homogeneous_frac*100)}_{gen_i}.png' if homogeneous_frac is not None\
                else f'{path}/{gen_i}.png'
    plt.savefig(save_file)
    plt.close()

def __plot_genotype_distribution(
        population: Population,
        param_names: tuple[str],
        run_i, gen_i, homogeneous_frac=None):
    param_hierarchy = __get_path_hierarchy(param_names, run_i) + ['genotype']
    path = '/'.join(param_hierarchy)
    if homogeneous_frac is not None:
        path = os.path.join(path, 'homogeneous')

    if not os.path.exists(path):
        os.makedirs(path)

    ones_counts = [len([True for gene in geno if gene == b'1']) for geno in population.genotypes]
    (x, y) = __get_distribution(ones_counts, x_max=population.fitness_function.chr_length)
    plt.bar(x, y)
    plt.xlabel('Number of 1s in genotype')
    plt.ylabel('Number of chromosomes')
    save_file = f'{path}/{int(homogeneous_frac*100)}_{gen_i}.png' if homogeneous_frac is not None\
                else f'{path}/{gen_i}.png'
    plt.savefig(save_file)
    plt.close()

def __get_distribution(data, x_min=0, x_max=None, x_step=1):
    if x_max is None:
        x_max = max(data)

    x = np.arange(x_min, x_max + x_step, x_step)
    y = np.zeros_like(x)
    for val in data:
        idx = int(round((val - x_min) / x_step))
        idx = max(0, min(idx, len(x)-1))
        y[idx] += 1

    return (x, y)

def __get_path_hierarchy(param_names, run_i):
    return [
        OUTPUT_FOLDER,
        'graphs',
        param_names[0], # fitness function
        param_names[1], # selection method
        str(N),
        param_names[2], # genetic operator
        param_names[3], # initial population
        str(run_i)
    ]