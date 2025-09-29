import numpy as np
from ga_core import (
    ga_run, fit_onemax, fit_leading_ones, save_plot, compute_stats, write_stats_md,
    PROBLEMS, DIM_LIST, RUNS, POP_FACTOR, ELITE_FRAC, P_MUT
)

from readme_generator import create_readme

SELECTIONS = ["roulette", "rank"]

def run_all():
    for problem in PROBLEMS:
        fitness = fit_onemax if problem == "onemax" else fit_leading_ones
        name = "OneMax" if problem == "onemax" else "LeadingOnes"
        for D in DIM_LIST:
            rows_for_md = []
            for selection in SELECTIONS:
                runs_hist, finals = [], []
                for _ in range(RUNS):
                    hist, fin = ga_run(D, fitness, selection)
                    runs_hist.append(hist); finals.append(fin)
                runs_hist = np.stack(runs_hist, 0); finals = np.array(finals)
                mean_curve, std_curve = runs_hist.mean(0), runs_hist.std(0)
                title = f"{name} – D={D} – sel={selection}, pop≈{int(POP_FACTOR*D)}, elite={ELITE_FRAC}, pmut={P_MUT}"
                save_plot(mean_curve, std_curve, title, problem, D, selection)
                rows_for_md.append((selection, compute_stats(finals)))
            write_stats_md(problem, D, rows_for_md)

if __name__ == "__main__":
    run_all()
    create_readme()
