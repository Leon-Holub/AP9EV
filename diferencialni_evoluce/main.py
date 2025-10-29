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


def get_bounds(func):
    if func.__name__ == "sphere":
        return -100, 100
    elif func.__name__ == "rastrigin":
        return -5.12, 5.12
    elif func.__name__ == "rosenbrock":
        return -2.048, 2.048
    elif func.__name__ == "schwefel":
        return -500, 500
    else:
        return -10, 10


if __name__ == "__main__":
    dim = 10
    func_to_use = schwefel
    bounds = get_bounds(func_to_use)
    max_evals = 10000
    pop = 40

    # 1) DE/rand/1/bin
    de_rand = DifferentialEvolution(
        func=func_to_use, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="rand1bin", F=0.5, CR=0.8
    )
    best, best_fit, log = de_rand.run()
    print(f"[{func_to_use.__name__}] DE/rand/1/bin: best_fit={best_fit:.3e}")
    de_rand.plot_convergence(f"{func_to_use.__name__} - DE/rand/1/bin", f"charts/{func_to_use.__name__}_rand1bin.png")

    # 2) DE/best/1/bin
    de_best = DifferentialEvolution(
        func=func_to_use, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="best1bin", F=0.5, CR=0.8
    )
    best, best_fit, log = de_best.run()
    print(f"[{func_to_use.__name__}] DE/best/1/bin: best_fit={best_fit:.3e}")
    de_best.plot_convergence(f"{func_to_use.__name__} - DE/best/1/bin", f"charts/{func_to_use.__name__}_best1bin.png")

    # 3) jDE (rand/1)
    de_jde = DifferentialEvolution(
        func=func_to_use, dim=dim, bounds=bounds,
        pop_size=pop, max_evals=max_evals,
        strategy="rand1bin", F=0.5, CR=0.9,
        jde=True, tau1=0.1, tau2=0.1
    )
    best, best_fit, log = de_jde.run()
    print(f"[{func_to_use.__name__}] jDE (rand/1): best_fit={best_fit:.3e}")
    de_jde.plot_convergence(f"{func_to_use.__name__} - jDE (rand/1)", f"charts/{func_to_use.__name__}_jde.png")
