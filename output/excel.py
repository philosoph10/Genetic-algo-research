from config import N, NR, OUTPUT_FOLDER, RUN_STATS_NAMES, EXP_STATS_NAMES, FCONSTALL_RUN_STATS_NAMES, FCONSTALL_EXP_STATS_NAMES
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
    worksheet.freeze_panes(2, 2)
    
    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        row = exp_i + 2
        worksheet.write(row, 0, experiment_stats.params[1])
        worksheet.write(row, 1, experiment_stats.params[2])

        run_stats_count = len(run_stats_names)
        for run_i, run_stats in enumerate(experiment_stats.runs):
            for stat_i, stat_name in enumerate(run_stats_names):
                col = run_i * run_stats_count + stat_i + 2
                worksheet.write(row, col, getattr(run_stats, stat_name))
                if exp_i == 0:
                    worksheet.write(1, col, stat_name)

            if exp_i == 0:
                start_col = run_i * run_stats_count + 2
                worksheet.merge_range(0, start_col, 0, start_col + run_stats_count - 1, f'Run {run_i}', merge_format)

        for stat_i, stat_name in enumerate(exp_stats_names):
            col = run_stats_count * NR + stat_i + 2
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                    worksheet.write(1, col, stat_name)

        if exp_i == 0:
            start_col = run_stats_count * NR + 2
            worksheet.merge_range(0, start_col, 0, start_col + len(exp_stats_names) - 1, f'Aggregated', merge_format)
            worksheet.merge_range(0, 0, 1, 0, 'Selection Method', merge_format)
            worksheet.merge_range(0, 1, 1, 1, 'Genetic Operator', merge_format)
       
    workbook.close()
    

def write_aggregated_stats(experiment_stats_list: list[ExperimentStats]):
    path = f'{OUTPUT_FOLDER}/tables'
    filename = f'aggregated_{N}.xlsx'

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(f'{path}/{filename}')
    worksheet = workbook.add_worksheet()
    worksheet.name = 'aggregated'
    worksheet.freeze_panes(1, 3)

    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        if exp_i == 0:
            worksheet.write(0, 0, 'Fitness Function')
            worksheet.write(0, 1, 'Selection Method')
            worksheet.write(0, 2, 'Genetic Operator')

        row = exp_i + 1
        worksheet.write(row, 0, experiment_stats.params[0])
        worksheet.write(row, 1, experiment_stats.params[1])
        worksheet.write(row, 2, experiment_stats.params[2])
        
        for stat_i, stat_name in enumerate(EXP_STATS_NAMES):
            col = stat_i + 3
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                worksheet.write(0, col, stat_name)

    workbook.close()
