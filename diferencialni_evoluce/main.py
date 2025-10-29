from de_core import DifferentialEvolution
import numpy as np
import math


def sphere(x):
    return np.sum(x * x)


def rastrigin(x):
    return 10 * len(x) + np.sum(x * x - 10 * np.cos(2 * math.pi * x))


def rosenbrock(x):
    return sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def schwefel(x):
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))


FUNCTION_BOUNDS = {
    sphere: (-100, 100),
    rastrigin: (-5.12, 5.12),
    rosenbrock: (-2.048, 2.048),
    schwefel: (-500, 500),
}


def get_bounds(func):
    return FUNCTION_BOUNDS.get(func, (-10, 10))


def run_multiple_runs(de_params, runs=10):
    logs = []
    final_fits = []

    for r in range(runs):
        de = DifferentialEvolution(**de_params, seed=np.random.randint(0, 10000))
        best, best_fit, log = de.run()
        logs.append(np.array(log))
        final_fits.append(best_fit)
        print(f"Best vector sample ({label}): {best[:3]}")

    min_len = min(len(l) for l in logs)
    logs = [l[:min_len] for l in logs]
    mean_curve = np.mean([l[:, 1] for l in logs], axis=0)
    evals = logs[0][:, 0]
    return evals, mean_curve, final_fits


if __name__ == "__main__":
    dim = 10
    max_evals = 10000
    pop = 50
    runs = 10

    for function in FUNCTION_BOUNDS.keys():
        func_to_use = function
        bounds = get_bounds(func_to_use)

        strategies = [
            ("DE/rand/1/bin", dict(
                func=func_to_use, dim=dim, bounds=bounds,
                pop_size=pop, max_evals=max_evals,
                strategy="rand1bin", F=0.5, CR=0.8
            )),
            ("DE/best/1/bin", dict(
                func=func_to_use, dim=dim, bounds=bounds,
                pop_size=pop, max_evals=max_evals,
                strategy="best1bin", F=0.5, CR=0.8
            )),
            ("jDE (rand/1)", dict(
                func=func_to_use, dim=dim, bounds=bounds,
                pop_size=pop, max_evals=max_evals,
                strategy="rand1bin", F=0.5, CR=0.9,
                jde=True, tau1=0.1, tau2=0.1
            )),
        ]

        comparison_results = []

        for label, params in strategies:
            evals, mean_curve, final_fits = run_multiple_runs(params, runs=runs)
            mean = np.mean(final_fits)
            min_val = np.min(final_fits)
            print(f"[{func_to_use.__name__}] {label}: "
                  f"avg_final={mean:.3e}, best_final={min_val:.3e}")

            log = np.column_stack((evals, mean_curve))
            comparison_results.append((log, f"{label} - {min_val:.3e}"))

        DifferentialEvolution.plot_comparison(
            comparison_results,
            title=f"Porovnání konvergence (průměr z {runs} běhů) – {func_to_use.__name__}",
            out_path=f"charts/{func_to_use.__name__}_comparison_avg.png"
        )
