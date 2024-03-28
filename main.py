from config import env, NR
from model.fitness_functions import *
from selection.rws import *
from selection.sus import *
from model.encoding import *
from model.gen_operators import *
from output import excel
from runner import run_experiment
from datetime import datetime
import time


def centered_scaling(ps: float):
    return lambda arr: -(np.mean(arr)*ps - np.max(arr)) / (ps - 1)

if env == 'test':
    fitness_functions = [
        # (FconstALL(100), 'FconstALL'),
        (FH(BinaryEncoder(100)), 'FH'),
        # (Fx2(FloatEncoder(0.0, 10.23, 10)), 'Fx2')
    ]
    selection_methods = [
        # (RWS(), 'RWS'),
        # (SUS(), 'SUS'),
        (ScaledRWS(1., np.mean), 'Mean RWS'),
        # (ScaledSUS(1., centered_scaling(1.2)), 'Centred SUS, ps=1.2')
    ]
    gen_operators = [
        (BlankGenOperator, 'no_operators')
    ]
    population_inits = [
        # (0, 'no optimal chromosomes'),
        # (1, '1 optimal chromosome'),
        (0.1, "10% optimal chromosomes")
    ]
else:
    fitness_functions = [
        (FconstALL(100), 'FconstALL'),
        (FHD(100, 100), 'FHD'),
        (Fx2(FloatEncoder(0.0, 10.23, 10)), 'Fx2'),
        (Fx2(FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fx2_gray'),
        (F5122subx2(FloatEncoder(-5.12, 5.11, 10)), 'F5122subx2'),
        (F5122subx2(FloatEncoder(-5.12, 5.11, 10, is_gray=True)), 'F5122subx2_gray'),
        (Fexp(0.25, FloatEncoder(0.0, 10.23, 10)), 'Fexp0.25'),
        (Fexp(0.25, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp0.25_gray'),
        (Fexp(1, FloatEncoder(0.0, 10.23, 10)), 'Fexp1'),
        (Fexp(1, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp1_gray'),
        (Fexp(2, FloatEncoder(0.0, 10.23, 10)), 'Fexp2'),
        (Fexp(2, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp2_gray')
    ]
    selection_methods = [
        (RWS, 'RWS'),
        (DisruptiveRWS, 'RWS_disruptive'),
        (SUS, 'SUS'),
        (DisruptiveSUS, 'SUS_disruptive'),
        (ScaledRWS(1., np.mean), 'Mean RWS'),
        (ScaledSUS(1., np.mean), 'Mean SUS'),
        (ScaledRWS(1., np.median), 'Median RWS'),
        (ScaledRWS(1., centered_scaling(1.2)), 'Centered RWS, ps=1.2'),
        (ScaledRWS(1., centered_scaling(1.6)), 'Centered RWS, ps=1.6'),
        (ScaledRWS(1., centered_scaling(2)), 'Centered RWS, ps=2')
    ]
    gen_operators = [
        (BlankGenOperator, 'no_operators'),
        (Crossover, 'crossover'),
        (Mutation, 'mutation'),
        (CrossoverAndMutation, 'xover_mut')
    ]

# a list of tuples of parameters for each run that involves a certain fitness function 
# {fitness_func_name: [(tuples with run parameters), (), ..., ()], other_func: [], ...}
experiment_params = {
    ff: [
        (sm, go, pi, (ff_name, sm_name, go_name, pi_name))
        for (sm, sm_name) in selection_methods
        for (go, go_name) in gen_operators
        for (pi, pi_name) in population_inits
    ] for (ff, ff_name) in fitness_functions
}

# only keeping one list of populations in memory at a time (for one fitness function)
def generate_all_populations_for_fitness_function(ff, n_optimal=1):
    return [ff.generate_population_for_run(run_i, n_optimal=n_optimal) for run_i in range(NR)]

def log(x):
    datetime_prefix = str(datetime.now())[:-4]
    print(f'{datetime_prefix} | {x}')

def validate_params(ff: FitnessFunc, sm: SelectionMethod, go: GeneticOperator, pi, param_names: list) -> bool:
    """
    validate the parameter set with respect to population initialization
    """
    if isinstance(ff, FconstALL) and pi == 0:
        return True
    if isinstance(ff, FconstALL) and (not isinstance(pi, int) or pi != 1):
        return False
    if issubclass(go, BlankGenOperator) and pi == 0:
        return False
    return True


if __name__ == '__main__':
    log('Program start')
    print('----------------------------------------------------------------------')
    start_time = time.time()
    results = []

    for ff in experiment_params:
        ff_start_time = time.time()
        # get experiment parameters for a given running configuration
        exp_params = experiment_params[ff]

        # generate populations for each each initialization configuration
        populations = {
            pi: generate_all_populations_for_fitness_function(ff, n_optimal=pi)
            for (pi, name) in population_inits
        }

        # filter out the configurations that are not required
        exp_params = [param for param in exp_params if validate_params(ff, *param)]

        # add respective populations to each parameter configuration
        # params[2] is the population initialization parameter
        params = [params + (populations[params[2]],) for params in exp_params]
        if len(params) == 0:
            continue
        # print(f'function = {ff}')
        # for i, param in enumerate(params):
        #     print(f'param[{i}] = {param}')
        experiment_stats_list = [run_experiment(*p) for p in params]

        excel.write_ff_stats(experiment_stats_list)
        for experiment_stats in experiment_stats_list:
            del experiment_stats.runs
            results.append(experiment_stats)

        ff_end_time = time.time()
        ff_name = experiment_params[ff][0][3][0]
        log(f'{ff_name} experiments finished in {(ff_end_time - ff_start_time):.2f}s')

    excel.write_aggregated_stats(results)

    print('----------------------------------------------------------------------')
    end_time = time.time()
    log(f'Program end. Total runtime: {end_time - start_time:.2f}s')
