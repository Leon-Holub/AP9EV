# main_experiment.py

import os
import csv
import time
import numpy as np
import matplotlib.pyplot as plt

from ga_core import GAReal
from de_core import DifferentialEvolution
from pso_core import PSO


# ---------------------------------------------------------
# Testovací funkce
# ---------------------------------------------------------

def sphere(x):
    return np.sum(x ** 2)


def rosenbrock(x):
    return np.sum(
        100 * (x[1:] - x[:-1] ** 2) ** 2 +
        (1 - x[:-1]) ** 2
    )


def schwefel(x):
    return 418.9829 * len(x) - np.sum(
        x * np.sin(np.sqrt(np.abs(x)))
    )

def rastrigin(x):
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))

PROBLEMS = {
    "sphere":     {"fn": sphere,     "bounds": (-5.12, 5.12)},
    "rosenbrock": {"fn": rosenbrock, "bounds": (-5.0, 10.0)},
    "schwefel":   {"fn": schwefel,   "bounds": (-500.0, 500.0)},
    "rastrigin": {"fn": rastrigin, "bounds": (-5.12, 5.12)},
}


# ---------------------------------------------------------
# Directory setup
# ---------------------------------------------------------

def ensure_dirs():
    os.makedirs("results/raw", exist_ok=True)
    os.makedirs("tables", exist_ok=True)
    os.makedirs("charts", exist_ok=True)


# ---------------------------------------------------------
# Algorithm factories
# ---------------------------------------------------------

def make_algorithms():
    def ga_factory(func, dim, bounds, max_evals, seed):
        return GAReal(
            func=func,
            dim=dim,
            bounds=bounds,
            pop_size=200,
            max_evals=max_evals,
            elite_frac=0.1,
            p_mut=0.1,
            sigma_frac=0.05,
            seed=seed,
        )

    def de_rand_factory(func, dim, bounds, max_evals, seed):
        return DifferentialEvolution(
            func=func, dim=dim, bounds=bounds,
            pop_size=50, max_evals=max_evals,
            strategy="rand1bin", F=0.5, CR=0.8,
            jde=False, seed=seed,
        )

    def de_best_factory(func, dim, bounds, max_evals, seed):
        return DifferentialEvolution(
            func=func, dim=dim, bounds=bounds,
            pop_size=50, max_evals=max_evals,
            strategy="best1bin", F=0.5, CR=0.8,
            jde=False, seed=seed,
        )

    def jde_factory(func, dim, bounds, max_evals, seed):
        return DifferentialEvolution(
            func=func, dim=dim, bounds=bounds,
            pop_size=50, max_evals=max_evals,
            strategy="rand1bin", F=0.5, CR=0.9,
            jde=True, tau1=0.1, tau2=0.1,
            seed=seed,
        )

    def pso_linear_factory(func, dim, bounds, max_evals, seed):
        return PSO(
            func=func, dim=dim,
            lower=bounds[0], upper=bounds[1],
            npop=40, max_fes=max_evals,
            w_strategy="linear", w_max=0.8, w_min=0.3,
            c1=2.0, c2=2.0,
            topology="global",
            seed=seed,
        )

    def pso_const_global_factory(func, dim, bounds, max_evals, seed):
        return PSO(
            func=func, dim=dim,
            lower=bounds[0], upper=bounds[1],
            npop=40, max_fes=max_evals,
            w_strategy="const", w_const=0.7,
            c1=1.49618, c2=1.49618,
            topology="global",
            seed=seed,
        )

    def pso_const_ring_factory(func, dim, bounds, max_evals, seed):
        return PSO(
            func=func, dim=dim,
            lower=bounds[0], upper=bounds[1],
            npop=40, max_fes=max_evals,
            w_strategy="const", w_const=0.6,
            c1=1.49618, c2=1.49618,
            topology="ring",
            seed=seed,
        )

    algorithms = {
        "GA_real_gauss": ga_factory,
        "DE_rand1bin": de_rand_factory,
        "DE_best1bin": de_best_factory,
        "jDE_rand1bin": jde_factory,
        "PSO_linear_global": pso_linear_factory,
        "PSO_const_global": pso_const_global_factory,
        "PSO_const_ring": pso_const_ring_factory,
    }

    return algorithms


# ---------------------------------------------------------
# CSV helper functions
# ---------------------------------------------------------

def load_existing_runs(path):
    if not os.path.exists(path):
        return []
    values = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            values.append(float(row["best_value"]))
    return values


def append_csv(path, run_id, best_value, runtime_sec):
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["run", "best_value", "runtime_sec"])
        writer.writerow([run_id, best_value, runtime_sec])


# ---------------------------------------------------------
# Convergence graph for ONE function+dimension
# ---------------------------------------------------------

def generate_convergence_chart_single(dim, fname):
    algorithms = list(make_algorithms().keys())

    plt.figure(figsize=(10, 6))

    for algo_name in algorithms:
        histories = []

        # load all histories
        for run_id in range(11):
            hist_path = f"results/raw/D{dim}_{fname}_{algo_name}_run{run_id}_history.csv"
            if not os.path.exists(hist_path):
                continue

            evals, vals = [], []
            with open(hist_path, "r") as f:
                next(f)
                for line in f:
                    e, v = line.strip().split(",")
                    evals.append(float(e))
                    vals.append(float(v))

            histories.append((evals, vals))

        if len(histories) == 0:
            continue

        # unify length
        min_len = min(len(h[0]) for h in histories)
        xs = histories[0][0][:min_len]
        matrix = np.array([h[1][:min_len] for h in histories])

        # compute mean only
        mean_curve = matrix.mean(axis=0)

        # *** ONLY MEAN LINE ***
        plt.plot(xs, mean_curve, label=algo_name, linewidth=2)

    plt.title(f"Convergence – D={dim}, function={fname}")
    plt.xlabel("FES")
    plt.ylabel("Best-so-far (log)")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()

    out_path = f"charts/D{dim}_{fname}_convergence.png"
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"  → Graf hotov: {out_path}")




# ---------------------------------------------------------
# Summary for ONE function+dimension
# ---------------------------------------------------------

def save_summary_single(dim, fname):
    algorithms = list(make_algorithms().keys())
    out_path = f"tables/D{dim}_{fname}_summary.md"

    stats = []  # (algo_name, mean, std, median, min, max, mean_time)

    # načteme data
    for algo_name in algorithms:
        csv_path = f"results/raw/D{dim}_{fname}_{algo_name}.csv"
        if not os.path.exists(csv_path):
            continue

        vals, times = [], []
        with open(csv_path, "r") as fcsv:
            reader = csv.DictReader(fcsv)
            for row in reader:
                vals.append(float(row["best_value"]))
                times.append(float(row["runtime_sec"]))

        vals, times = np.array(vals), np.array(times)

        stats.append((
            algo_name,
            vals.mean(),
            vals.std(),
            np.median(vals),
            vals.min(),
            vals.max(),
            times.mean()
        ))

    # najdeme nejlepší (nejnižší mean)
    if len(stats) > 0:
        best_mean = min(s[1] for s in stats)
    else:
        best_mean = None

    # vytvoříme tabulku
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Summary – D={dim}, Function={fname}\n\n")
        f.write("| Algorithm | Mean | Std.Dev. | Median | Min | Max | Mean time [s] |\n")
        f.write("|-----------|------|----------|--------|-----|------|----------------|\n")

        for algo_name, mean, std, median, amin, amax, mean_time in stats:

            is_best = (mean == best_mean)

            if is_best:
                # tučný řádek
                f.write(
                    f"| **{algo_name}** | "
                    f"**{mean:.6e}** | **{std:.6e}** | **{median:.6e}** | "
                    f"**{amin:.6e}** | **{amax:.6e}** | **{mean_time:.2f}** |\n"
                )
            else:
                f.write(
                    f"| {algo_name} | "
                    f"{mean:.6e} | {std:.6e} | {median:.6e} | "
                    f"{amin:.6e} | {amax:.6e} | {mean_time:.2f} |\n"
                )

    print(f"  → Tabulka hotova (best bold): {out_path}")



# ---------------------------------------------------------
# Main Experiment Loop
# ---------------------------------------------------------

def run_experiments(runs=11):
    ensure_dirs()
    rng = np.random.default_rng(12345)
    algorithms = make_algorithms()
    dims = [10, 20]

    for dim in dims:
        max_evals = 10_000 * dim
        print(f"\n===== D = {dim} – max evals = {max_evals} =====")

        for fname, pdata in PROBLEMS.items():
            func = pdata["fn"]
            bounds = pdata["bounds"]
            print(f"\n  Funkce: {fname}")

            # nejprve dopočítáme všechny algoritmy
            for algo_name, factory in algorithms.items():
                print(f"    Algoritmus: {algo_name}")

                csv_path = f"results/raw/D{dim}_{fname}_{algo_name}.csv"
                existing = load_existing_runs(csv_path)
                done = len(existing)

                print(f"      Hotových běhů: {done}/{runs}")

                if done < runs:
                    for run_id in range(done, runs):
                        seed = int(rng.integers(0, 10_000_000))
                        opt = factory(func, dim, bounds, max_evals, seed)

                        start = time.time()
                        out = opt.run()
                        runtime_sec = time.time() - start

                        if isinstance(opt, GAReal):
                            best_fit, history = out
                        else:
                            _, best_fit, history = out

                        append_csv(csv_path, run_id, best_fit, runtime_sec)

                        hist_path = f"results/raw/D{dim}_{fname}_{algo_name}_run{run_id}_history.csv"
                        with open(hist_path, "w", newline="", encoding="utf-8") as hf:
                            writer = csv.writer(hf)
                            writer.writerow(["eval", "best_so_far"])
                            for e, b in history:
                                writer.writerow([e, b])

                        print(f"        -> run {run_id}: {best_fit:.4e}  ({runtime_sec:.2f} sec)")

            # když všechny algoritmy doběhly → vytvoříme graf + tabulku
            print(f"\n  Generuji graf konvergence pro {fname} (D={dim})...")
            generate_convergence_chart_single(dim, fname)

            print(f"  Generuji summary tabulku pro {fname} (D={dim})...")
            save_summary_single(dim, fname)

    print("\n=== Všechny výpočty dokončeny ===")


# ---------------------------------------------------------
# MAIN ENTRY
# ---------------------------------------------------------

if __name__ == "__main__":
    run_experiments(runs=11)
