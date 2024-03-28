from config import N, NR, OUTPUT_FOLDER, RUN_STATS_NAMES, EXP_STATS_NAMES, FCONSTALL_RUN_STATS_NAMES, FCONSTALL_EXP_STATS_NAMES, DISTRIBUTIONS_TO_PLOT, GEN_STATS_NAMES, FCONSTALL_GEN_STATS_NAMES
import xlsxwriter
import os
from stats.experiment_stats import ExperimentStats

def write_ff_stats(experiment_stats_list: list[ExperimentStats]):
    ff_name = experiment_stats_list[0].params[0]
    path = f'{OUTPUT_FOLDER}/tables/{ff_name}'
    filename = f'{ff_name}_{N}.xlsx'

    if ff_name == 'FconstALL':
        run_stats_names = FCONSTALL_RUN_STATS_NAMES
        exp_stats_names = FCONSTALL_EXP_STATS_NAMES
    else:
        run_stats_names = RUN_STATS_NAMES
        exp_stats_names = EXP_STATS_NAMES

    if not os.path.exists(path):
        os.makedirs(path)
    
    workbook = xlsxwriter.Workbook(f'{path}/{filename}')
    worksheet = workbook.add_worksheet()
    worksheet.name = ff_name
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': 'yellow'})
    worksheet.freeze_panes(2, 3)
    
    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        # print(f"!!!!\n\tExperiment stats = {experiment_stats.params}\n!!!!")
        row = exp_i + 2
        worksheet.write(row, 0, experiment_stats.params[1])
        worksheet.write(row, 1, experiment_stats.params[2])
        worksheet.write(row, 2, experiment_stats.params[3])

        run_stats_count = len(run_stats_names)
        for run_i, run_stats in enumerate(experiment_stats.runs):
            for stat_i, stat_name in enumerate(run_stats_names):
                col = run_i * run_stats_count + stat_i + 3
                worksheet.write(row, col, getattr(run_stats, stat_name))
                if exp_i == 0:
                    worksheet.write(1, col, stat_name)

            if exp_i == 0:
                start_col = run_i * run_stats_count + 3
                worksheet.merge_range(0, start_col, 0, start_col + run_stats_count - 1, f'Run {run_i}', merge_format)

        for stat_i, stat_name in enumerate(exp_stats_names):
            col = run_stats_count * NR + stat_i + 3
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                    worksheet.write(1, col, stat_name)

        if exp_i == 0:
            start_col = run_stats_count * NR + 3
            worksheet.merge_range(0, start_col, 0, start_col + len(exp_stats_names) - 1, f'Aggregated', merge_format)
            worksheet.merge_range(0, 0, 1, 0, 'Selection Method', merge_format)
            worksheet.merge_range(0, 1, 1, 1, 'Genetic Operator', merge_format)
            worksheet.merge_range(0, 2, 1, 2, 'Initial Population', merge_format)
       
    workbook.close()
    

def write_aggregated_stats(experiment_stats_list: list[ExperimentStats]):
    path = f'{OUTPUT_FOLDER}/tables'
    filename = f'aggregated_{N}.xlsx'

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(f'{path}/{filename}')
    worksheet = workbook.add_worksheet()
    worksheet.name = 'aggregated'
    worksheet.freeze_panes(1, 4)

    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        if exp_i == 0:
            worksheet.write(0, 0, 'Fitness Function')
            worksheet.write(0, 1, 'Selection Method')
            worksheet.write(0, 2, 'Genetic Operator')
            worksheet.write(0, 3, 'Initial Population')

        row = exp_i + 1
        worksheet.write(row, 0, experiment_stats.params[0])
        worksheet.write(row, 1, experiment_stats.params[1])
        worksheet.write(row, 2, experiment_stats.params[2])
        worksheet.write(row, 3, experiment_stats.params[3])
        
        for stat_i, stat_name in enumerate(EXP_STATS_NAMES):
            col = stat_i + 4
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                worksheet.write(0, col, stat_name)

    workbook.close()

def write_generation_stats(generation_stats_list, param_names, run_i):
    """
    Write statistics of a generation to excel
    :param generation_stats_list: list of generation statistics
    :param param_names: list of parameters, defining the path
    :param run_i: number of the run of the GA
    """
    path = __get_path_hierarchy(param_names, run_i)
    path = os.path.join(*path)
    os.makedirs(path, exist_ok=True)
    filename = f'{run_i}.xlsx'

    workbook = xlsxwriter.Workbook(os.path.join(path, filename))
    worksheet = workbook.add_worksheet()
    worksheet.name = f'Run: {run_i}'
    worksheet.freeze_panes(1, 1)

    worksheet.write(0, 0, 'Generation number')
    if param_names[0] != 'FconstALL':
        for col in range(len(GEN_STATS_NAMES)):
            worksheet.write(0, col + 1, GEN_STATS_NAMES[col])

        for i in range(DISTRIBUTIONS_TO_PLOT):
            row = i + 1
            gen_stats = generation_stats_list[i]
            # write generation number
            worksheet.write(row, 0, i + 1)
            for col in range(len(GEN_STATS_NAMES)):
                worksheet.write(row, col + 1, getattr(gen_stats, GEN_STATS_NAMES[col]))
    else:
        for col in range(len(FCONSTALL_GEN_STATS_NAMES)):
            worksheet.write(0, col + 1, FCONSTALL_GEN_STATS_NAMES[col])

        for i in range(DISTRIBUTIONS_TO_PLOT):
            row = i + 1
            gen_stats = generation_stats_list[i]
            # write generation number
            worksheet.write(row, 0, i + 1)
            for col in range(len(FCONSTALL_GEN_STATS_NAMES)):
                worksheet.write(row, col + 1, getattr(gen_stats, FCONSTALL_GEN_STATS_NAMES[col]))
    
    workbook.close()

def __get_path_hierarchy(param_names, run_i):
    return [
        OUTPUT_FOLDER,
        'tables',
        param_names[0], # fitness function
        str(N),
        param_names[1], # selection method
        param_names[2], # genetic operator
        param_names[3], # initial population
        str(run_i)
    ]
