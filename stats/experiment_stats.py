from config import NR
from stats.run_stats import RunStats
import numpy as np

class ExperimentStats:
    def __init__(self, experiment_params: tuple[str]):
        self.params = experiment_params
        self.runs = np.empty(NR, dtype=object)

        self.Suc = 0
        self.N_Suc = 0
        self.Min_NI = None
        self.Max_NI = None
        self.Avg_NI = None
        self.Sigma_NI = None

        # Non-Successful but Convergent Runs
        self.nonSuc = None
        self.nonMin_NI = None
        self.nonMax_NI = None
        self.nonAvg_NI = None
        self.nonSigma_NI = None
        self.nonAvg_F_found = None
        self.nonSigma_F_found = None
        self.nonMax_F_found = None

        # Loss of Optimal Chromosome
        self.NI_with_Lose = None
        self.Avg_NI_lose = None
        self.Sigma_NI_lose = None
        self.Avg_Num_lose = None
        self.Sigma_Num_lose = None
        self.Avg_optSaved_NI_lose = None
        self.Sigma_optSaved_NI_lose = None
        self.Avg_MaxOptSaved_NI_lose = None
        self.Sigma_MaxOptSaved_NI_lose = None

        # Reproduction Rate
        self.Min_RR_min = None
        self.NI_RR_min = None
        self.Max_RR_max = None
        self.NI_RR_max = None
        self.Avg_RR_min = None
        self.Avg_RR_max = None
        self.Avg_RR_avg = None
        self.Sigma_RR_min = None
        self.Sigma_RR_max = None
        self.Sigma_RR_avg = None
        self.Avg_RR_start = None
        self.Avg_RR_fin = None
        self.Sigma_RR_start = None
        self.Sigma_RR_fin = None
        self.Min_RR_start = None
        self.Max_RR_start = None

        # Loss of Diversity
        self.Min_Teta_min = None
        self.NI_Teta_min = None
        self.Max_Teta_max = None
        self.NI_Teta_max = None
        self.Avg_Teta_min = None
        self.Avg_Teta_max = None
        self.Avg_Teta_avg = None
        self.Sigma_Teta_min = None
        self.Sigma_Teta_max = None
        self.Sigma_Teta_avg = None
        self.Avg_Teta_start = None
        self.Avg_Teta_fin = None
        self.Sigma_Teta_start = None
        self.Sigma_Teta_fin = None
        self.Min_Teta_start = None
        self.Max_Teta_start = None

        # Unique chromosomes
        self.Avg_unique_X_start = None
        self.Avg_unique_X_fin = None
        self.Sigma_unique_X_start = None
        self.Sigma_unique_X_fin = None
        self.Min_unique_X_start = None
        self.Max_unique_X_start = None
        self.Min_unique_X_fin = None
        self.Max_unique_X_fin = None

        # Selection Intensity
        self.Min_I_min = None
        self.NI_I_min = None
        self.Max_I_max = None
        self.NI_I_max = None
        self.Avg_I_min = None
        self.Avg_I_max = None
        self.Avg_I_avg = None
        self.Sigma_I_min = None
        self.Sigma_I_max = None
        self.Sigma_I_avg = None
        self.Min_I_start = None
        self.Max_I_start = None
        self.Avg_I_start = None
        self.Sigma_I_start = None

        # Selection Difference
        self.Min_s_min = None
        self.NI_s_min = None
        self.Max_s_max = None
        self.NI_s_max = None
        self.Avg_s_min = None
        self.Avg_s_max = None
        self.Avg_s_avg = None
        self.Min_s_start = None
        self.Max_s_start = None
        self.Avg_s_start = None
        self.Sigma_s_start = None

        # Growth Rate
        self.Min_GR_early = None
        self.Max_GR_early = None
        self.Avg_GR_early = None
        self.Min_GR_late = None
        self.Max_GR_late = None
        self.Avg_GR_late = None
        self.Min_GR_avg = None
        self.Max_GR_avg = None
        self.Avg_GR_avg = None
        self.Min_GR_start = None
        self.Max_GR_start = None
        self.Avg_GR_start = None
        self.Sigma_GR_start = None

        # Selection Pressure
        self.Min_Pr_min = None
        self.NI_Pr_min = None
        self.Max_Pr_max = None
        self.NI_Pr_max = None
        self.Avg_Pr_min = None
        self.Avg_Pr_max = None
        self.Avg_Pr_avg = None
        self.Sigma_Pr_min = None
        self.Sigma_Pr_max = None
        self.Sigma_Pr_avg = None
        self.Min_Pr_start = None
        self.Max_Pr_start = None
        self.Avg_Pr_start = None
        self.Sigma_Pr_start = None

        # Fisher's Exact Test for Selection Pressure
        self.Min_Fish_min = None
        self.NI_Fish_min = None
        self.Max_Fish_max = None
        self.NI_Fish_max = None
        self.Avg_Fish_min = None
        self.Avg_Fish_max = None
        self.Avg_Fish_avg = None
        self.Sigma_Fish_min = None
        self.Sigma_Fish_max = None
        self.Sigma_Fish_avg = None
        self.Min_Fish_start = None
        self.Max_Fish_start = None
        self.Avg_Fish_start = None
        self.Sigma_Fish_start = None

        # Kendall's Tau-b Test for Selection Pressure
        self.Min_Kend_min = None
        self.NI_Kend_min = None
        self.Max_Kend_max = None
        self.NI_Kend_max = None
        self.Avg_Kend_min = None
        self.Avg_Kend_max = None
        self.Avg_Kend_avg = None
        self.Sigma_Kend_min = None
        self.Sigma_Kend_max = None
        self.Sigma_Kend_avg = None
        self.Min_Kend_start = None
        self.Max_Kend_start = None
        self.Avg_Kend_start = None
        self.Sigma_Kend_start = None

    def add_run(self, run: RunStats, run_i):
        self.runs[run_i] = run

    def calculate(self):
        successful_runs = [run for run in self.runs if run.is_successful]
        self.N_Suc = len(successful_runs)
        self.Suc = self.N_Suc / NR

        self.__calculate_convergence_stats(successful_runs)
        self.__calculate_rr_stats(successful_runs)
        self.__calculate_teta_stats(successful_runs)
        self.__calculate_unique_X_stats(successful_runs)

        if self.params[0] != 'FconstALL':
            self.__calculate_loss_stats(self.runs)
            
            non_successful_convergent_runs = [run for run in self.runs 
                                          if (not run.is_successful and run.has_converged)]
            self.N_nonSuc = len(non_successful_convergent_runs)
            self.nonSuc = self.N_nonSuc / NR

            self.__calculate_s_stats(successful_runs)
            self.__calculate_i_stats(successful_runs)
            self.__calculate_gr_stats(successful_runs)
            self.__calculate_pr_stats(successful_runs)
            self.__calculate_fish_stats(successful_runs)
            self.__calculate_kend_stats(successful_runs)
            self.__calculate_non_suc_stats(non_successful_convergent_runs)


    def __calculate_convergence_stats(self, runs: list[RunStats]):
        NIs = [run.NI for run in runs]
        if NIs:
            self.Min_NI = min(NIs)
            self.Max_NI = max(NIs)
            self.Avg_NI = np.mean(NIs)
            self.Sigma_NI = np.std(NIs)
    
    def __calculate_loss_stats(self, runs: list[RunStats]):
        NI_lose_list = [run.NI_lose for run in runs if run.Num_lose > 0]
        self.NI_with_Lose = len(NI_lose_list)
        if NI_lose_list:
            self.Avg_NI_lose = np.mean(NI_lose_list)
            self.Sigma_NI_lose = np.std(NI_lose_list)
        Num_lose_list = [run.Num_lose for run in runs if run.Num_lose > 0]
        if Num_lose_list:
            self.Avg_Num_lose = np.mean(Num_lose_list)
            self.Sigma_Num_lose = np.std(Num_lose_list)
        optSaved_NI_lose_list = [run.optSaved_NI_lose for run in runs if run.Num_lose > 0]
        if optSaved_NI_lose_list:
            self.Avg_optSaved_NI_lose = np.mean(optSaved_NI_lose_list)
            self.Sigma_optSaved_NI_lose = np.std(optSaved_NI_lose_list)
        MaxOptSaved_NI_lose_list = [run.MaxOptSaved_NI_lose for run in runs if run.Num_lose > 0]
        if MaxOptSaved_NI_lose_list:
            self.Avg_MaxOptSaved_NI_lose = np.mean(MaxOptSaved_NI_lose_list)
            self.Sigma_MaxOptSaved_NI_lose = np.std(MaxOptSaved_NI_lose_list)

    def __calculate_rr_stats(self, runs: list[RunStats]):
        RR_min_list = [run.RR_min for run in runs]
        if RR_min_list:
            run_i_RR_min = np.argmin(RR_min_list)
            self.NI_RR_min = runs[run_i_RR_min].NI_RR_min
            self.Min_RR_min = RR_min_list[run_i_RR_min]
            self.Avg_RR_min = np.mean(RR_min_list)
            self.Sigma_RR_min = np.std(RR_min_list)
        RR_max_list = [run.RR_max for run in runs]
        if RR_max_list:
            run_i_RR_max = np.argmax(RR_max_list)
            self.NI_RR_max = runs[run_i_RR_max].NI_RR_max
            self.Max_RR_max = RR_max_list[run_i_RR_max]
            self.Avg_RR_max = np.mean(RR_max_list)
            self.Sigma_RR_max = np.std(RR_max_list)
        RR_avg_list = [run.RR_avg for run in runs]
        if RR_avg_list:
            self.Avg_RR_avg = np.mean(RR_avg_list)
            self.Sigma_RR_avg = np.std(RR_avg_list)
        RR_start_list = [run.RR_start for run in runs]
        if RR_start_list:
            self.Avg_RR_start = np.mean(RR_start_list)
            self.Sigma_RR_start = np.std(RR_start_list)
            self.Min_RR_start = min(RR_start_list)
            self.Max_RR_start = max(RR_start_list)
        RR_fin_list = [run.RR_fin for run in runs]
        if RR_fin_list:
            self.Avg_RR_fin = np.mean(RR_fin_list)
            self.Sigma_RR_fin = np.std(RR_fin_list)

    def __calculate_teta_stats(self, runs: list[RunStats]):
        Teta_min_list = [run.Teta_min for run in runs]
        if Teta_min_list:
            run_i_Teta_min = np.argmin(Teta_min_list)
            self.NI_Teta_min = runs[run_i_Teta_min].NI_Teta_min
            self.Min_Teta_min = Teta_min_list[run_i_Teta_min]
            self.Avg_Teta_min = np.mean(Teta_min_list)
            self.Sigma_Teta_min = np.std(Teta_min_list)
        Teta_max_list = [run.Teta_max for run in runs]
        if Teta_max_list:
            run_i_Teta_max = np.argmax(Teta_max_list)
            self.NI_Teta_max = runs[run_i_Teta_max].NI_Teta_max
            self.Max_Teta_max = Teta_max_list[run_i_Teta_max]
            self.Avg_Teta_max = np.mean(Teta_max_list)
            self.Sigma_Teta_max = np.std(Teta_max_list)
        Teta_avg_list = [run.Teta_avg for run in runs]
        if Teta_avg_list:
            self.Avg_Teta_avg = np.mean(Teta_avg_list)
            self.Sigma_Teta_avg = np.std(Teta_avg_list)
        Teta_start_list = [run.Teta_start for run in runs]
        if Teta_start_list:
            self.Avg_Teta_start = np.mean(Teta_start_list)
            self.Sigma_Teta_start = np.std(Teta_start_list)
            self.Min_Teta_start = min(Teta_start_list)
            self.Max_Teta_start = max(Teta_start_list)
        Teta_fin_list = [run.Teta_fin for run in runs]
        if Teta_fin_list:
            self.Avg_Teta_fin = np.mean(Teta_fin_list)
            self.Sigma_Teta_fin = np.std(Teta_fin_list)

    def __calculate_unique_X_stats(self, runs: list[RunStats]):
        unique_X_start_list = [run.unique_X_start for run in runs]
        if unique_X_start_list:
            self.Avg_unique_X_start = np.mean(unique_X_start_list)
            self.Sigma_unique_X_start = np.std(unique_X_start_list)
            self.Min_unique_X_start = min(unique_X_start_list)
            self.Max_unique_X_start = max(unique_X_start_list)
        unique_X_fin_list = [run.unique_X_fin for run in runs]
        if unique_X_fin_list:
            self.Avg_unique_X_fin = np.mean(unique_X_fin_list)
            self.Sigma_unique_X_fin = np.std(unique_X_fin_list)
            self.Min_unique_X_fin = min(unique_X_fin_list)
            self.Max_unique_X_fin = max(unique_X_fin_list)

    def __calculate_s_stats(self, runs: list[RunStats]):
        s_min_list = [run.s_min for run in runs]
        if s_min_list:
            run_i_s_min = np.argmin(s_min_list)
            self.NI_s_min = runs[run_i_s_min].NI_s_min
            self.Min_s_min = s_min_list[run_i_s_min]
            self.Avg_s_min = np.mean(s_min_list)
        s_max_list = [run.s_max for run in runs]
        if s_max_list:
            run_i_s_max = np.argmax(s_max_list)
            self.NI_s_max = runs[run_i_s_max].NI_s_max
            self.Max_s_max = s_max_list[run_i_s_max]
            self.Avg_s_max = np.mean(s_max_list)
        s_avg_list = [run.s_avg for run in runs]
        if s_avg_list:
            self.Avg_s_avg = np.mean(s_avg_list)
        s_start_list = [run.s_start for run in runs]
        if s_start_list:
            self.Min_s_start = min(s_start_list)
            self.Max_s_start = max(s_start_list)
            self.Avg_s_start = np.mean(s_start_list)
            self.Sigma_s_start = np.std(s_start_list)

    def __calculate_i_stats(self, runs: list[RunStats]):
        I_min_list = [run.I_min for run in runs]
        if I_min_list:
            run_i_I_min = np.argmin(I_min_list)
            self.NI_I_min = runs[run_i_I_min].NI_I_min
            self.Min_I_min = I_min_list[run_i_I_min]
            self.Avg_I_min = np.mean(I_min_list)
            self.Sigma_I_min = np.std(I_min_list)
        I_max_list = [run.I_max for run in runs]
        if I_max_list:
            run_i_I_max = np.argmax(I_max_list)
            self.NI_I_max = runs[run_i_I_max].NI_I_max
            self.Max_I_max = I_max_list[run_i_I_max]
            self.Avg_I_max = np.mean(I_max_list)
            self.Sigma_I_max = np.std(I_max_list)
        I_avg_list = [run.I_avg for run in runs]
        if I_avg_list:
            self.Avg_I_avg = np.mean(I_avg_list)
            self.Sigma_I_avg = np.std(I_avg_list)
        I_start_list = [run.I_start for run in runs]
        if I_start_list:
            self.Min_I_start = min(I_start_list)
            self.Max_I_start = max(I_start_list)
            self.Avg_I_start = np.mean(I_start_list)
            self.Sigma_I_start = np.std(I_start_list)

    def __calculate_gr_stats(self, runs: list[RunStats]):
        gre_list = [run.GR_early for run in runs if run.GR_early is not None]
        grl_list = [run.GR_late for run in runs if run.GR_late is not None]
        gra_list = [run.GR_avg for run in runs if run.GR_avg is not None]
        grs_list = [run.GR_start for run in runs if run.GR_start is not None]
        if gre_list:
            self.Avg_GR_early = np.mean(gre_list)
            self.Min_GR_early = min(gre_list)
            self.Max_GR_early = max(gre_list)
        if grl_list:
            self.Avg_GR_late = np.mean(grl_list)
            self.Min_GR_late = min(grl_list)
            self.Max_GR_late = max(grl_list)
        if gra_list:
            self.Avg_GR_avg = np.mean(gra_list)
            self.Min_GR_avg = min(gra_list)
            self.Max_GR_avg = max(gra_list)
        if grs_list:
            self.Min_GR_start = min(grs_list)
            self.Max_GR_start = max(grs_list)
            self.Avg_GR_start = np.mean(grs_list)
            self.Sigma_GR_start = np.std(grs_list)
        
    def __calculate_pr_stats(self, runs: list[RunStats]):
        pr_min_list = [run.Pr_min for run in runs]
        pr_max_list = [run.Pr_max for run in runs]
        pr_avg_list = [run.Pr_avg for run in runs]
        pr_start_list = [run.Pr_start for run in runs]
        if pr_min_list:
            self.Min_Pr_min = min(pr_min_list)
            self.NI_Pr_min = np.argmin(pr_min_list)
            self.Avg_Pr_min = np.mean(pr_min_list)
            self.Sigma_Pr_min = np.std(pr_min_list)
        if pr_max_list:
            self.Max_Pr_max = max(pr_max_list)
            self.NI_Pr_max = np.argmax(pr_max_list)
            self.Avg_Pr_max = np.mean(pr_max_list)
            self.Sigma_Pr_max = np.std(pr_max_list)
        if pr_avg_list:
            self.Avg_Pr_avg = np.mean(pr_avg_list)
            self.Sigma_Pr_avg = np.std(pr_avg_list)
        if pr_start_list:
            self.Min_Pr_start = min(pr_start_list)
            self.Max_Pr_start = max(pr_start_list)
            self.Avg_Pr_start = np.mean(pr_start_list)
            self.Sigma_Pr_start = np.std(pr_start_list)
    
    def __calculate_fish_stats(self, runs: list[RunStats]):
        fish_min_list = [run.Fish_min for run in runs]
        fish_max_list = [run.Fish_max for run in runs]
        fish_avg_list = [run.Fish_avg for run in runs]
        fish_start_list = [run.Fish_start for run in runs]
        if fish_min_list:
            self.Min_Fish_min = min(fish_min_list)
            self.NI_Fish_min = np.argmin(fish_min_list)
            self.Avg_Fish_min = np.mean(fish_min_list)
            self.Sigma_Fish_min = np.std(fish_min_list)
        if fish_max_list:
            self.Max_Fish_max = max(fish_max_list)
            self.NI_Fish_max = np.argmax(fish_max_list)
            self.Avg_Fish_max = np.mean(fish_max_list)
            self.Sigma_Fish_max = np.std(fish_max_list)
        if fish_avg_list:
            self.Avg_Fish_avg = np.mean(fish_avg_list)
            self.Sigma_Fish_avg = np.std(fish_avg_list)
        if fish_start_list:
            self.Min_Fish_start = min(fish_start_list)
            self.Max_Fish_start = max(fish_start_list)
            self.Avg_Fish_start = np.mean(fish_start_list)
            self.Sigma_Fish_start = np.std(fish_start_list)
    
    def __calculate_kend_stats(self, runs: list[RunStats]):
        kend_min_list = [run.Kend_min for run in runs]
        kend_max_list = [run.Kend_max for run in runs]
        kend_avg_list = [run.Kend_avg for run in runs]
        kend_start_list = [run.Kend_start for run in runs]
        if kend_min_list:
            self.Min_Kend_min = min(kend_min_list)
            self.NI_Kend_min = np.argmin(kend_min_list)
            self.Avg_Kend_min = np.mean(kend_min_list)
            self.Sigma_Kend_min = np.std(kend_min_list)
        if kend_max_list:
            self.Max_Kend_max = max(kend_max_list)
            self.NI_Kend_max = np.argmax(kend_max_list)
            self.Avg_Kend_max = np.mean(kend_max_list)
            self.Sigma_Kend_max = np.std(kend_max_list)
        if kend_avg_list:
            self.Avg_Kend_avg = np.mean(kend_avg_list)
            self.Sigma_Kend_avg = np.std(kend_avg_list)
        if kend_start_list:
            self.Min_Kend_start = min(kend_start_list)
            self.Max_Kend_start = max(kend_start_list)
            self.Avg_Kend_start = np.mean(kend_start_list)
            self.Sigma_Kend_start = np.std(kend_start_list)
    
    def __calculate_non_suc_stats(self, runs: list[RunStats]):
        nonNIs = [run.NI for run in runs]
        if nonNIs:
            self.nonMin_NI = min(nonNIs)
            self.nonMax_NI = max(nonNIs)
            self.nonAvg_NI = np.mean(nonNIs)
            self.nonSigma_NI = np.std(nonNIs)
        F_found_list = [run.F_found for run in runs]
        if F_found_list:
            self.nonAvg_F_found = np.mean(F_found_list)
            self.nonSigma_F_found = np.std(F_found_list)
            self.nonMax_F_found = max(F_found_list)


    def __str__(self):
        return ("Suc: " + str(self.Suc) + "%" +
                "\nMin: " + str(self.Min_NI) + "\nMax: " + str(self.Max_NI) + "\nAvg: " + str(self.Avg_NI))
